from flask import Flask, render_template, request, redirect, jsonify
import re
import subprocess
import threading
import os

app = Flask(__name__)

# Global variables to store log content and discovery thread
log_content = []
discovery_thread = None
stop_event = threading.Event()

# Function to discover child URLs using curl and regex
def discover_subdirectories(base_url):
    global stop_event
    if not base_url.startswith(('http://', 'https://')):
        base_url = base_url

    directories_to_check = [base_url]
    
    sanitized_base_url = base_url.replace('/', '_').replace(':', '_')
    log_file = f"{sanitized_base_url}_url_scanner_program_paths.log"

    if os.path.exists(log_file):
        log_content.append(f"Warning: The log file {log_file} already exists and will be overwritten.")

    with open(log_file, 'w') as log:
        log.write(f"Base URL: {base_url}\n")

        def get_links(url):
            try:
                response = subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', url], capture_output=True, text=True)
                return response.stdout
            except Exception as e:
                log_content.append(f"Error fetching URL: {url}, {e}")
                return ""

        while directories_to_check:
            if stop_event.is_set():  # Check if the stop event is set
                log_content.append("=" * 68)
                log_content.append("Discovery process has been stopped.")
                log_content.append("=" * 68)
                return log_file, True  # Indicate that the process was stopped

            current_dir = directories_to_check.pop(0)

            # Log with separators
            log_content.append("=" * 68)
            log_content.append(f"Checking paths in: {current_dir}")
            log_content.append("=" * 68)

            response_content = get_links(current_dir)
            links = re.findall(r'href=["\'](.*?)["\']', response_content)

            if links:
                log_content.append("=" * 68)
                log_content.append(f"Found paths in {current_dir}:")
                log_content.append("=" * 68)

                for link in sorted(set(links)):
                    if link.startswith('/'):
                        full_url = current_dir + link
                    else:
                        full_url = f"{'/'.join(current_dir.split('/')[:-1])}/{link}"
                    
                    log.write(f"{full_url}\n")
                    
                    if link.endswith('/'):
                        log_content.append(f"Subdirectory: {full_url}")
                        directories_to_check.append(full_url)
                    else:
                        log_content.append(f"File: {full_url}")
            else:
                log_content.append("=" * 68)
                log_content.append(f"No files or subdirectories found in: {current_dir}")
                log_content.append("=" * 68)

        log_content.append("=" * 68)
        log_content.append(f"All validated URLs have been logged to {log_file}")
        log_content.append("=" * 68)

    return log_file, False  # Indicate that the process completed normally

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        # Execute the curl command
        try:
            result = subprocess.check_output(['curl', '-vsIL', url], stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
    return render_template('index.html', result=result)

# Handle form submission and URL discovery
@app.route('/discover', methods=['POST'])
def discover():
    global discovery_thread, stop_event
    base_url = request.form['url']
    stop_event.clear()  # Clear the stop event before starting a new discovery

    discovery_thread = threading.Thread(target=discover_subdirectories, args=(base_url,))
    discovery_thread.start()

    return redirect('/')  # Redirect to the home page

# Handle the curl request for another route
@app.route('/curl', methods=['GET', 'POST'])
def curl_request():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        # Execute the curl command
        try:
            result = subprocess.check_output(['curl', '-vsIL', url], stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
    return render_template('index.html', result=result)
    
# Return log content
@app.route('/log')
def get_log_content():
    return {'content': log_content}

# Stop the discovery process
@app.route('/stop-discovery', methods=['POST'])
def stop_discovery():
    global stop_event
    stop_event.set()  # Signal to stop the discovery process
    return '', 204  # No content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

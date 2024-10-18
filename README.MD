# URL Discovery & Curl Testing App

## AUTHOR: GUSTAVO WYDLER AZUAGA
## VERSION: 1
## RELEASE DATE: 10-18-2024

A web application designed to discover child or subdomains from a given URL and perform curl tests to check the status of URLs. Built with Flask, this application offers a simple interface to execute and manage URL discovery and curl commands.

## Features

- **URL Discovery:** Input a URL to discover its child or subdomains.
- **Curl Command Execution:** Execute curl commands to check the status of a specified URL.
- **Live Log Output:** View real-time logs of discovery and curl command results.
- **Stop Discovery:** An option to halt ongoing discovery processes.

## Technologies Used

- **Flask:** A lightweight web framework for Python to handle server-side logic.
- **HTML/CSS:** For structuring and styling the web application interface.
- **JavaScript:** To manage asynchronous fetching of log content and interaction with the server.
- **Bootstrap:** (optional) For a responsive and visually appealing UI (if included in your project).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/url_discovery_curl_app.git
   cd url_discovery_curl_app

2. **Create and activate a python venv:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the requirements**
   
   ```bash
    pip install -r requirements.txt

5. **Depending on your system, you need to allow port 5000 through the firewall:**

   ```bash
   # For RHEL based systems:

   sudo firewall-cmd --permanent --add-port=5000/tcp
   sudo firewall-cmd --reload
   
   #For DEBIAN based systems (like Ubuntu):

   sudo ufw allow 5000/tcp
   sudo ufw reload

6. **Run the Application**

   Start the Flask development server:
   ```bash
    python3.8 2. **Create and activate a python venv:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the requirements**
   
   ```bash
    pip install -r requirements.txt

5. **Depending on your system, you need to allow port 5000 through the firewall:**

   ```bash
   # For RHEL based systems:

   sudo firewall-cmd --permanent --add-port=5000/tcp
   sudo firewall-cmd --reload
   
   #For DEBIAN based systems (like Ubuntu):

   sudo ufw allow 5000/tcp
   sudo ufw reload

6. **Run the Application**

   Start the Flask development server:
   ```bash
    python3.8 app.py

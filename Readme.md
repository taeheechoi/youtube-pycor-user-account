# Epicor Automation using Python - Creating and disabling user account from Gmail

<!-- ABOUT THE PROJECT -->

## About The Project

This project is for the Youtube channel Pycor where developers can learn how to integrate with Epicor ERP software in Python. 

The intention of this project is to help developers to automate user creation and deactivation in Epicor based on the emails received from HRIS system.

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- Python 3
- Python Packages: requests (2.28.1), Python-dotenv (0.20.0)
- VS Code

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/taeheechoi/youtube-pycor-user-account.git .
   ```
2. Create a virtual environment and activate it
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install packages
   ```sh
   pip install -r requirements.txt
   ```
4. Rename .env-example to .env and configure it
   ```
   GMAIL_ACCOUNT=Gmail account
   GMAIL_PASSWORD=Gmail app password
   IMAP_SERVER=imap.gmail.com
   EPICOR_USERID=Epicor user account
   EPICOR_PASSWORD=Epicor user password
   EPICOR_API_URL=https://Server/Environment/api/v1
   ```

## Acknowledgments

- [How to read emails in python](https://www.techgeekbuzz.com/blog/how-to-read-emails-in-python/)
- [Best readme template](https://github.com/othneildrew/Best-README-Template)

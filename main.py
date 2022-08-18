import email
import json
import logging
import os
from imaplib import IMAP4_SSL

import requests
from dotenv import load_dotenv

load_dotenv()

IMAP_SERVER = os.getenv('IMAP_SERVER')
GMAIL_ACCOUNT = os.getenv('GMAIL_ACCOUNT')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
EPICOR_USERID = os.getenv('EPICOR_USERID')
EPICOR_PASSWORD = os.getenv('EPICOR_PASSWORD')
EPICOR_API_URL = os.getenv('EPICOR_API_URL')


def get_user_name(name):
    # to create user name in Epicor, first character of first name + last name, if middle name is excluded

    first_name, last_name = name.split()[0], name.split()[-1]
    user_name = (first_name[0]+last_name).lower()
    return user_name


def get_employment_email(subject, search_words):
    # gets emails with subject including "New Employee" or "Employee Separation"

    with IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
        mail.select()

        response, data = mail.search(None, f'(SUBJECT "{subject}" UNSEEN)')
        employee_names = []

        if response == 'OK':
            for num in data[0].split():
                response, data = mail.fetch(num, '(RFC822)')  # OK, data

                if response == 'OK':
                    _, bytes_data = data[0]

                    message = email.message_from_bytes(bytes_data)

                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            message = part.get_payload(decode=True).decode()

                            start_index = message.index(search_words[0]) + len(search_words[0])
                            end_index = message.index(search_words[1])

                            full_name = message[start_index:end_index].strip()

                            employee_names.append(full_name)

            return employee_names
        return None


def get_data(url):
    # To get user data from Epicor

    response = requests.get(url, auth=(EPICOR_USERID, EPICOR_PASSWORD))

    if response.status_code == 200:
        return response.json()
    else:
        return None


def create_data(url, data):
    # To create a new employee in Epicor

    response = requests.post(url, auth=(EPICOR_USERID, EPICOR_PASSWORD), data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    user_name = data.get('UserID')

    if response.status_code == 201:
        logging.info(f'User account {user_name} has been created')
    else:
        logging.info(f'User account {user_name} is not created due to {response.content.decode()}')


def update_data(url, data):
    # To update user status  in Epicor

    response = requests.patch(url, auth=(EPICOR_USERID, EPICOR_PASSWORD), data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    user_name = data.get('UserID')

    if response.status_code == 204:
        logging.info(f'User account {user_name} has been disabled')
    else:
        logging.info(f'User account {user_name} is not disabled due to {response.content.decode()}')


def create_user_account(employee):
    URL = f'{EPICOR_API_URL}/Ice.BO.UserFileSvc/UserFiles'

    user_name = get_user_name(employee)

    payload = {
        "UserID": user_name,
        "Name": employee,
        "EMailAddress": f'{user_name}@test.com'
    }

    create_data(URL, payload)


def disable_user_account(user_name):
    URL = f'{EPICOR_API_URL}/Ice.BO.UserFileSvc/UserFiles({user_name})'

    response = get_data(URL)

    if response:
        payload = {
            "UserID": user_name,
            "UserDisabled": True
        }

        update_data(URL, payload)


if __name__ == '__main__':

    logging.basicConfig(filename='log/user_account.txt', format='%(asctime)s %(message)s', level=logging.INFO)

    # get new employees emails from gmail
    new_employees = get_employment_email('New Employee', ['Name: ', 'Start Date: '])

    if (new_employees):
        for employee in new_employees:
            create_user_account(employee)

    # get separated employees emails from gmail
    separated_employees = get_employment_email('Employee Separation', ['Name: ', 'End Date: '])

    if (separated_employees):
        for employee in separated_employees:
            user_name = get_user_name(employee)
            disable_user_account(user_name)

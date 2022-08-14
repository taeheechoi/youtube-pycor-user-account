from imaplib import IMAP4_SSL
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import email

load_dotenv()

IMAP_SERVER = os.getenv('IMAP_SERVER')
FROM_EMAIL = os.getenv('FROM_EMAIL')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
EPICOR_USERID = os.getenv('EPICOR_USERID')
EPICOR_PASSWORD = os.getenv('EPICOR_PASSWORD')
EPICOR_API_URL = os.getenv('EPICOR_API_URL')

def get_user_name(name):
    first_name, last_name = name.split()[0], name.split()[-1]
    user_name = (first_name[0]+last_name).lower()
    return user_name

def get_employment_email(subject, search_words):
    with IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(FROM_EMAIL, GMAIL_PASSWORD)
        mail.select()

        response, data = mail.search(None, f'(SUBJECT "{subject}")')
        names = []
        if response == 'OK':

            for num in data[0].split():
                response, data = mail.fetch(num, '(RFC822)')  # OK, data
                if response == 'OK':
                    _, bytes_data = data[0]

                    message = email.message_from_bytes(bytes_data)

                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            message = part.get_payload(decode=True).decode()
                            
                            start_index = message.index(search_words[0])+ len(search_words[0])
                            end_index = message.index(search_words[1])
                            
                            full_name = message[start_index:end_index].strip()

                            names.append(full_name)
            return names
        return None

def create_user_account_epicor(user_name):
    URL = f'{EPICOR_API_URL}/Erp.BO.SalesOrderSvc/SalesOrders'


if __name__ == '__main__':

    new_employees = get_employment_email('New Employee', ['Name: ', 'Start Date: '])
    
    if(new_employees):
        for employee in new_employees:
            user_name = get_user_name(employee)
            print(user_name)
    
    separated_employees = get_employment_email('Employee Separation', ['Name: ', 'End Date: '])
    
    if(separated_employees):
        for employee in separated_employees:
            user_name = get_user_name(employee)
            print(user_name)

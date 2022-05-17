import os
from ... import db
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL')
BRANCH_ID = os.getenv('BRANCH_ID')
SMS_ENDPOINT_URL = os.getenv('SMS_ENDPOINT_URL')

def check_date(branch_id: str, date: str):
    r = requests.get(f'{API_URL}/schedules/{branch_id}/{date}')
    if (r.status_code == 200):
        return True
    return False

def load_dates():
    available_slots = list()
    for date in ReservedDates.select():
        if check_date(date.branch_id, date.date):
            available_slots.append(date)
    if available_slots:
        find_owners(available_slots)

def find_owners(available_slots: list):
    for date in available_slots:
        for person in Person.select().where(Person.reserved_date_id == date.id):
            send_sms(person.phone_number)

def send_sms(phone_number: str): 
    print(f"Notified {phone_number}")
        

if __name__ == '__main__':
    load_dates()
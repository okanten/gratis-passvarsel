import os
from peewee import *
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL')
BRANCH_ID = os.getenv('BRANCH_ID')
SMS_ENDPOINT_URL = os.getenv('SMS_ENDPOINT_URL')


db = SqliteDatabase('dates.db')

class ReservedDates(Model):
    branch_id = CharField()
    date = DateField()
    
    class Meta:
        database = db


class Person(Model):
    reserved_date_id = ForeignKeyField(ReservedDates, backref='dates')
    phone_number = CharField()

    class Meta:
        database = db

db.connect()

db.create_tables([ReservedDates, Person])


date1 = ReservedDates(branch_id=BRANCH_ID, date="2022-07-07")
date1.save()

date2 = ReservedDates(branch_id=BRANCH_ID, date="2022-06-07")
date2.save()


test_person = Person(reserved_date_id=date1, phone_number="00000000")
test_person.save()


test_person2 = Person(reserved_date_id=date2, phone_number="00000001")
test_person2.save()

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
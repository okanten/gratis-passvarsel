from peewee import *
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SqliteDatabase('database.db')


class Branches(Model):
    branch_identifier = CharField(null=False, unique=True)
    
    class Meta:
        database = db


class User(Model):
    phone_number = CharField(null=False, unique=True)
    password = CharField(null=False)
    activated = BooleanField(null=False, default=False)

    class Meta:
        database = db

class ReservedDates(Model):
    branch_id = ForeignKeyField(Branches, backref="branch")
    user_id = ForeignKeyField(User, backref="owner")
    date = DateField()
    
    class Meta:
        database = db


def create_user(phone_number: str, password: str):
    try: 
        hashed_password = generate_password_hash(password)
        User(phone_number=phone_number, password=hashed_password).save()
        return True
    except IntegrityError:
        return False

def check_if_user_exists(phone_number: str):
    try:
        return User.get(User.phone_number == phone_number)
    except DoesNotExist:
        return False
        

def check_if_user_exists(phone_number: str):
    try:
        return User.get(User.phone_number == phone_number)
        return True
    except DoesNotExist:
        return False

def check_if_user_exists_id(id: int):
    try:
        User.get(User.id == id)
        return True
    except DoesNotExist:
        return False

def verify_login(phone_number: str, password: str):
    try:
        user = User.get(User.phone_number == phone_number)
        if check_password_hash(user.password, password):
            return user
    except DoesNotExist:
        return False

def branch_exists(branch_identifier: str):
    try:
        Branches.get(Branches.branch_identifier == branch_identifier)
        return True
    except DoesNotExist:
        return False

def add_branch(branch_identifier: str):
    Branches(branch_identifier=branch_identifier).save()

def get_branch_id_from_branch_identifier(branch_identifier: str):
    if branch_exists(branch_identifier):
        return Branches.get(branch_identifier=branch_identifier)

def add_date(phone_number: str, date_str: str, branch: str):
    user = check_if_user_exists(phone_number)
    if user:
        if not branch_exists(branch):
            add_branch(branch)
        branch_id = get_branch_id_from_branch_identifier(branch)
        date_formatted = date.fromisoformat(date_str)
        ReservedDates(branch_id = branch_id.id, user_id=user.id, date=date_formatted).save()
            
        

db.connect()

db.create_tables([ReservedDates, User, Branches])

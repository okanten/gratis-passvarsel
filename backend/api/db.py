from peewee import *
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
        User.get(User.phone_number == phone_number)
        return True
    except DoesNotExist:
        return False

def verify_login(phone_number: str, password: str):
    try:
        user = User.get(User.phone_number == phone_number)
        return check_password_hash(user.password, password)
    except DoesNotExist:
        return False
    #return check_password_hash(user.password, password)

db.connect()

db.create_tables([ReservedDates, User, Branches])

import uuid
from mongoengine import *
import datetime


class User(Document):
    user_id = StringField(required=True, unique=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    phone_number = StringField(max_length=15, required=True, unique=True)
    address = StringField(required=True)
    pin = StringField(required=True, max_length=6)
    balance = IntField(default=0)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    updated_date = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'users'
    }

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()

        self.user_id = str(uuid.uuid4())
        self.updated_date = datetime.datetime.now()

        return super(User, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(User, self).update(**kwargs)

from mongoengine import *
import datetime
import uuid


class Transaction(Document):
    user_id = StringField(required=True)
    transaction_type = StringField(required=True)
    top_up_id = StringField()
    amount_top_up = IntField()
    payment_id = StringField()
    transfer_id = StringField()
    amount = IntField()
    balance_before = IntField(required=True, default=0)
    balance_after = IntField(required=True, default=0)
    remarks = StringField()
    status = StringField(required=True, default="SUCCESS")
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    updated_date = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'transactions'
    }

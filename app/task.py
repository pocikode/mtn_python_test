import uuid

from app import celery
from app.models import Transaction


# test celery
@celery.task(name='add_together')
def add_together(a, b):
    return a + b


def get_user_balance(user_id):
    balance = 0
    last_transaction = Transaction.objects(user_id=user_id).order_by('-created_date').first()
    if last_transaction:
        balance = last_transaction.balance_after

    return balance


@celery.task(name='topup')
def topup(user_id, amount):
    balance = get_user_balance(user_id)

    transaction = Transaction(user_id=user_id,
                              top_up_id=str(uuid.uuid4()),
                              amount_top_up=amount,
                              balance_before=balance,
                              balance_after=balance + amount,
                              transaction_type='CREDIT').save()

    return {'to_pup_id': transaction.top_up_id,
            'amount_top_up': transaction.amount_top_up,
            'balance_before': transaction.balance_before,
            'balance_after': transaction.balance_after,
            'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S')}


@celery.task(name='payment')
def payment(user_id, amount, remarks):
    balance = get_user_balance(user_id)

    if balance < amount:
        return False

    transaction = Transaction(user_id=user_id,
                              payment_id=str(uuid.uuid4()),
                              amount=amount,
                              remarks=remarks,
                              balance_before=balance,
                              balance_after=balance - amount,
                              transaction_type='DEBIT')

    transaction.save()

    return {'payment_id': transaction.payment_id,
            'amount': transaction.amount,
            'remarks': transaction.remarks,
            'balance_before': transaction.balance_before,
            'balance_after': transaction.balance_after,
            'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S')}


@celery.task(name='transfer')
def transfer(user_id, target_id, amount, remarks):
    balance = get_user_balance(user_id)

    if balance < amount:
        return False

    transaction = Transaction(user_id=user_id,
                              transfer_id=str(uuid.uuid4()),
                              amount=amount,
                              remarks=remarks,
                              balance_before=balance,
                              balance_after=balance - amount,
                              transaction_type='DEBIT')

    transaction.save()

    # topup target user
    topup.delay(target_id, amount)

    return {'transfer_id': transaction.transfer_id,
            'amount': transaction.amount,
            'remarks': transaction.remarks,
            'balance_before': transaction.balance_before,
            'balance_after': transaction.balance_after,
            'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S')}

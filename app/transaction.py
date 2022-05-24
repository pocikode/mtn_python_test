from flask import (Blueprint, request, jsonify)
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Transaction, User
from app.utils import json_response
from app import task

bp = Blueprint('transaction', __name__)


# for test
@bp.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    balance = 0
    last_transaction = Transaction.objects(user_id=get_jwt_identity()).order_by('-created_date').first()

    if last_transaction:
        balance = last_transaction.balance_after

    return json_response(result={'balance': balance})


@bp.route('/topup', methods=['POST'])
@jwt_required()
def topup():
    amount = request.json['amount']
    topup_task = task.topup.delay(get_jwt_identity(), amount)

    return json_response(result=topup_task.get())


@bp.route('/payment', methods=['POST'])
@jwt_required()
def payment():
    amount = request.json['amount']
    remark = request.json['remarks']
    payment_task = task.payment.delay(get_jwt_identity(), amount, remark)
    result = payment_task.get()

    if not result:
        return jsonify(message='Balance is not enough'), 400

    return json_response(result=payment_task.get())


@bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    amount = request.json['amount']
    remark = request.json['remarks']
    target_user_id = request.json['target_user']
    target_user = User.objects(user_id=target_user_id).first()

    if not target_user:
        return jsonify(message='Target user is invalid'), 400

    transfer_task = task.transfer.delay(get_jwt_identity(), target_user.user_id, amount, remark)
    result = transfer_task.get()

    if not result:
        return jsonify(message='Balance is not enough'), 400

    return json_response(result=transfer_task.get())


@bp.route('/transactions', methods=['GET'])
@jwt_required()
def report_transactions():
    transactions = Transaction.objects(user_id=get_jwt_identity()).order_by('-created_date')

    result = []
    for transaction in transactions:
        dummy = {}
        if transaction.top_up_id:
            dummy['top_up_id'] = transaction.top_up_id
        elif transaction.payment_id:
            dummy['payment_id'] = transaction.payment_id
        elif transaction.transfer_id:
            dummy['transfer_id'] = transaction.transfer_id

        dummy.update({'status': transaction.status,
                      'user_id': transaction.user_id,
                      'transaction_type': transaction.transaction_type,
                      'amount': transaction.amount_top_up if transaction.top_up_id else transaction.amount,
                      'remarks': transaction.remarks,
                      'balance_before': transaction.balance_before,
                      'balance_after': transaction.balance_after,
                      'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S')})

        result.append(dummy)

    return json_response(result=result)

from app.models import User
from flask import (Blueprint, request, jsonify)
from mongoengine.errors import NotUniqueError
from app.utils import json_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        user = User(**body).save()

        return json_response(result={
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'address': user.address,
            'created_date': user.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    except NotUniqueError:
        return jsonify(message="Phone Number already registered"), 400


@bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.objects(phone_number=body['phone_number'], pin=body['pin']).first()

    if not user:
        return jsonify(message='Phone number and pin doesn’t match.'), 401

    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(access_token)

    return json_response(result={'access_token': access_token, 'refresh_token': refresh_token})


@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():  # for test
    user_id = get_jwt_identity()
    user = User.objects(user_id=user_id).first()

    return jsonify(user)


@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    body = request.get_json()
    user_id = get_jwt_identity()

    user = User.objects(user_id=user_id).first()
    user.update(**body)

    return json_response(result={
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'address': user.address,
        'updated_date': user.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
    })

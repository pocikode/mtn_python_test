from flask import jsonify


def json_response(status='SUCCESS', result=None, code=200):
    return jsonify({
        'status': status,
        'result': result
    }), code

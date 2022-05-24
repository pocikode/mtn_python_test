import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from celery import Celery


celery = Celery(__name__, broker=os.environ.get('REDIS_URI'), backend=os.environ.get('REDIS_URI'))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGODB_SETTINGS={
            'host': os.environ.get('MONGO_URI')
        },
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET'),
        CELERY_CONFIG={
            'broker_url': os.environ.get('REDIS_URI'),
            'result_backend': os.environ.get('REDIS_URI')
        }
    )

    @app.route('/hello')
    def hello():
        return 'Hello World'

    # register db
    db = MongoEngine()
    db.init_app(app)

    # celery
    celery.conf.update(app.config['CELERY_CONFIG'])

    # setup JWT
    jwt = JWTManager(app)

    # register cli commands
    from . import cli as cli_app
    cli_app.init_app(app)

    # register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # register transaction blueprint
    from . import transaction
    app.register_blueprint(transaction.bp)

    return app

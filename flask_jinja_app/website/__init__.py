#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
DB_NAME = "KejaFlask"
DB_USER = "keja_flask_user"
DB_PASS = "kejaflask001"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_ECHO'] = "True"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://{}:{}@localhost:5000/{}".format(
        DB_USER, DB_PASS, DB_NAME)
    db.init_app(app)

    from website.models import Landlord, Tenant, House, Apartment
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'dev'
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(DB_NAME)
  db.init_app(app)

  return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None

def init_app(name):
    global app
    if app == None:
        app = Flask(name)
    return app

def get_app():
    # global app
    # if app == None:
    #     app = init_app(__name__)
    return app

db = None


def init_db():
    global db
    if db == None:
        db = SQLAlchemy()  # class db extends app
    return db


def get_db():
    global db
    if db == None:
        db = init_db()
    return db
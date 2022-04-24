from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None

def init_app(name):
    global app
    if app == None:
        app = Flask(name)
    return app

def get_app():
    global app
    if app == None:
        app = init_app(__name__)
    return app
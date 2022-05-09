import sys
print(sys.version)
from flask import render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from config import UPLOAD_FOLDER, SQLALCHEMY_DATABASE_URI, SECRET_KEY, MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, \
    MAIL_SUBJECT_PREFIX, MAIL_SENDER
# Rutas
from rutas.api.uni_api import uni_api
from rutas.api.empresa_api import empresa_api
from rutas.controllers.empresa_rutas import empresa_rutas
from rutas.api.session_handler import session_handler
from rutas.controllers.registry_handler import registry_handler
from rutas.controllers.pruebas import pruebas

from models import Empresa
from common.init import init_db, init_app


app = init_app(__name__)

from rutas.controllers.views import views

app.register_blueprint(views)
app.register_blueprint(uni_api)
app.register_blueprint(empresa_api)
app.register_blueprint(empresa_rutas)
app.register_blueprint(session_handler)
app.register_blueprint(registry_handler)
app.register_blueprint(pruebas)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = MAIL_SUBJECT_PREFIX
app.config['FLASKY_MAIL_SENDER'] = MAIL_SENDER

db = init_db()
db.init_app(app)

from common.mail import init_mail

mail = init_mail(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import utils.admin


@login_manager.user_loader
def load_user(company_id):
    return Empresa.query.get(company_id)


@app.route("/empresaajax")
def empresa_ajax():
    return render_template("empresa_ajax.html")


@app.route("/adminajax")
def admin_ajax():
    return render_template("admin_ajax.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)

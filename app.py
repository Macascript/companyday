from flask import render_template
from flask_login import LoginManager
from flask_migrate import Migrate

import config
from config import UPLOAD_FOLDER, SQLALCHEMY_DATABASE_URL, SECRET_KEY
from init import init_app
# Módulos
from models import Empresa, init_db
import views
from mail import init_mail
# Rutas
from api.uni_api import uni_api
from api.empresa_api import empresa_api
from api.empresa_rutas import empresa_rutas
from api.session_handler import session_handler
from api.registry_handler import registry_handler
#from api.pruebas import pruebas


app = init_app(__name__)

app.register_blueprint(uni_api)
app.register_blueprint(empresa_api)
app.register_blueprint(empresa_rutas)
app.register_blueprint(session_handler)
app.register_blueprint(registry_handler)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = config.MAIL_SUBJECT_PREFIX

db = init_db(app)
db.init_app(app)


mail = init_mail(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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

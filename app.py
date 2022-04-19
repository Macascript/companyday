from crypt import methods
# from curses import flash
import os
from flask import Flask, render_template, request, redirect, flash, url_for
import flask
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired

from extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
import json
from flask import jsonify


# Modelos
from models.actividad import Actividad
from models.asistente import Asistente
from models.charla import Charla
from models.empresa import Empresa
from models.pais import Pais
from models.poblacion import Poblacion
from models.presentacion import Presentacion
from models.provincia import Provincia
from models.sesion import Sesion
from models.speed_meeting import Speed_meeting

# Rutas
from rutas.uni_api import uni_api
from rutas.empresa_api import empresa_api
from rutas.empresa_rutas import empresa_rutas
from rutas.pruebas import pruebas

from extensions import UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:companyday@macascript.com/companyday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'clavedeprueba'


app.register_blueprint(uni_api)
app.register_blueprint(empresa_api)
app.register_blueprint(empresa_rutas)
app.register_blueprint(pruebas)

# db = SQLAlchemy(app)
db.init_app(app)

# CONTROLLER

@app.route("/plantilla")
def plantilla():
    return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def index():
    db.create_all()
    if request.method == "POST":
        if Empresa.query.filter_by(email=request.form["email"]).count() > 0:
            return render_template("nuevoIndex.html",state="EmailExists",empresas=empresas,paises=paises)
        # else: return jsonify({'loginState': 'EmailNoExists'})

        new_empresa = registrarEmpresa()
        db.session.add(new_empresa)
        print(new_empresa)

        if "feria_empresas" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["feria_empresas"])))
        if "presentacion" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["presentacion"])))
            presentacion = registrarPresentacion(request.form,new_empresa.id)
            db.session.add(presentacion)
            new_empresa.presentacion = presentacion
        if "speed_meetings" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["speed_meetings"])))
            speed_meeting = registrarSpeedMeeting(request.form,new_empresa.id)
            db.session.add(speed_meeting)
            new_empresa.speed_meeting = speed_meeting
        if "charlas" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["charlas"])))
            charla = registrarCharla(request.form,new_empresa.id)
            db.session.add(charla)
            new_empresa.charla = charla;
        
        db.session.commit()
        return redirect("/profile")
    return render_template("nuevoIndex.html",state="NotLogged")


class LoginForm(FlaskForm): # class RegisterForm extends FlaskForm
    email = StringField('Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    remember = BooleanField('Remember me')

@app.route('/login',methods=['GET','POST'])
def login():
    empresas = Empresa.query.all()
    paises = Pais.query.all()
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Empresa.query.filter(Empresa.email==form.email.data).first()
            if not user or not check_password_hash(user.contrasenya, form.password.data):
                flash("Wrong user or Password!")
            elif user.es_verificado:
                login_user(user, remember=form.remember.data)
                flash("Welcome back {}".format(current_user.username))
                return redirect(url_for('index'))
            else:
                flash("User not confirmed. Please visit your email to confirm your user.")
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route("/empresaajax")
def empresa_ajax():
    return render_template("empresa_ajax.html")

@app.route("/adminajax")
def admin_ajax():
    return render_template("admin_ajax.html")

def registrarEmpresa():
    print("prueba de si existe o no el objeto request: ")
    print(request)
    nombre = request.form["nombre"]
    print(nombre)
    nombre_persona_contacto = request.form["nombre_persona_contacto"]
    print(nombre_persona_contacto)
    email = request.form["email"]
    print(email)
    telefono = request.form["telefono"]
    print(telefono)
    direccion = request.form["direccion"]
    print(direccion)
    poblacion = Poblacion.query.filter_by(
        nombre = request.form["poblacion"],
        provincia_id = Provincia.query.filter_by(
            nombre = request.form["provincia"],
            pais_id = Pais.query.filter_by(
                nombre = request.form["pais"]
            ).first().id
        ).first().id
    ).first()
    print(poblacion)
    codigo_postal = request.form["codigo_postal"]
    print(codigo_postal)
    web = request.form["web"]
    print(web)
    logo_url = ""
    print("logo_url" in request.files)
    print("Esto es lo que hay dentro de files:")
    print(request.files.keys())
    # check if the post request has the file part
    if 'logo_url' in request.files:
        file = request.files['logo_url']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logo_url = UPLOAD_FOLDER+"/"+filename


    consentimiento_uso_nombre = request.form["consentimiento_uso_nombre"] == "si"
    print(consentimiento_uso_nombre)
    buscando_candidatos = request.form["buscando_candidatos"] == "si"
    print(buscando_candidatos)
    return Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,logo_url,consentimiento_uso_nombre,buscando_candidatos)

def registrarPresentacion(id):
    modalidad_presentacion = request.form["modalidad_presentacion"] == "presencial"
    print(modalidad_presentacion)
    animacion = "animacion" in request.form
    print(animacion)
    videojuegos = "videojuegos" in request.form
    print(videojuegos)
    disenio = "disenio" in request.form
    print(disenio)
    ingenieria = "ingenieria" in request.form
    print(ingenieria)
    return Presentacion(id,modalidad_presentacion,animacion,videojuegos,disenio,ingenieria)

def registrarSpeedMeeting(id):
    print("numero de sesiones = "+str(request.form["numero_sesiones"]))
    
    # preguntas = form["preguntas"]
    speed_meeting = Speed_meeting(id)
    for i in range(int(request.form["numero_sesiones"])):
        modalidad_speed_meeting = request.form["modalidad_speed_meeting_"+str(i)] == "presencial"
        descripcion_speed_meeting = request.form["descripcion_speed_meeting_"+str(i)]
        fecha_speed_meeting = request.form["fecha_speed_meeting_"+str(i)]
        fecha_speed_meeting = datetime.strptime(fecha_speed_meeting,"%Y-%m-%d")
        print(fecha_speed_meeting)
        duracion = request.form["duracion_"+str(i)]
        print(duracion)
        speed_meeting.sesiones.append(Sesion(id,modalidad_speed_meeting,descripcion_speed_meeting,fecha_speed_meeting,duracion))
    return speed_meeting

def registrarCharla(id):
    modalidad_charlas = request.form["modalidad_charlas"] == "presencial"
    descripcion = request.form["descripcion_charla"]
    fecha_charla = request.form["fecha_charla"]
    hora_charla = request.form["hora_charla"]
    fecha_hora_charla = datetime.strptime(fecha_charla+" "+hora_charla,"%Y-%m-%d %H:%M")
    # ponente = request.form["ponente"]
    return Charla(id,descripcion,modalidad_charlas,fecha_hora_charla,"ponente")

if __name__ == '__main__':
    app.run(port=5000,debug=True)

# END CONTROLLER END
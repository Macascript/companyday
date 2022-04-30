import random

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import LoginForm
from jinja2 import Environment
import os
import datetime

from init import get_app
from mail import send_email
from models import get_db, Empresa, Actividad, Poblacion, Presentacion, Pais, Provincia, Speed_meeting, Sesion, Charla
from config import UPLOAD_FOLDER

app = get_app()
db = get_db()


@app.route("/plantilla")
def plantilla():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    return render_template("nuevoIndex.html", state="NotLogged", form = form)


@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        new_empresa = registrarEmpresa()
        if new_empresa != None:
            db.session.add(new_empresa)
            if "feria_empresas" in request.form:
                new_empresa.actividades.append(Actividad.query.get(int(request.form["feria_empresas"])))
            if "presentacion" in request.form:
                new_empresa.actividades.append(Actividad.query.get(int(request.form["presentacion"])))
                presentacion = registrarPresentacion(new_empresa.id)
                db.session.add(presentacion)
                new_empresa.presentacion = presentacion
            if "speed_meetings" in request.form:
                new_empresa.actividades.append(Actividad.query.get(int(request.form["speed_meetings"])))
                speed_meeting = registrarSpeedMeeting(new_empresa.id)
                db.session.add(speed_meeting)
                new_empresa.speed_meeting = speed_meeting
            if "charlas" in request.form:
                new_empresa.actividades.append(Actividad.query.get(int(request.form["charlas"])))
                charla = registrarCharla(new_empresa.id)
                db.session.add(charla)
                new_empresa.charla = charla

            db.session.commit()


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = Empresa.query.filter(Empresa.email == form.email.data).first()
        print(form.email)
        print(user.contrasenya)
        if not user or not user.contrasenya == form.password.data:  # check_password_hash(user.contrasenya, form["password"]):
            flash("Wrong user or Password!")
        elif user.is_active:
            login_user(user, remember=True)
            flash("Welcome back {}".format(current_user.nombre))
            return redirect(url_for('index'))
        else:
            flash("User not confirmed. Please visit your email to confirm your user.")
            flash(current_user)
            login_user(user, remember=True)
            return redirect(url_for('index'))

    return redirect(url_for('index'))


def registrarEmpresa():
    if request:
        nombre = request.form["nombre"]
        nombre_persona_contacto = request.form["nombre_persona_contacto"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        poblacion = Poblacion.query.filter_by(
            nombre=request.form["poblacion"],
            provincia_id=Provincia.query.filter_by(
                nombre=request.form["provincia"],
                pais_id=Pais.query.filter_by(
                    nombre=request.form["pais"]
                ).first().id
            ).first().id
        ).first()
        codigo_postal = request.form["codigo_postal"]
        web = request.form["web"]
        logo_url = ""
        # check if the post request has the file part
        if 'logo_url' in request.files:
            file = request.files['logo_url']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo_url = UPLOAD_FOLDER + "/" + filename

        password_hashed = generate_password_hash(request.form.password.data, method="sha256")
        consentimiento_uso_nombre = request.form["consentimiento_uso_nombre"] == "si"
        buscando_candidatos = request.form["buscando_candidatos"] == "si"
        empresa = Empresa(nombre=nombre, nombre_persona_contacto=nombre_persona_contacto,
                          email=email, telefono=telefono,
                          direccion=direccion, poblacion=poblacion,
                          codigo_postal=codigo_postal, web=web,
                          logo_url=logo_url, consentimiento_uso_nombre=consentimiento_uso_nombre,
                          buscando_candidatos=buscando_candidatos, contrasenya=password_hashed,
                          user_hash=str(random.getrandbits(128))
                          )
        send_email(empresa.email, 'Porfavor confirme su correo electrónico', 'mail/new_empresa', user=empresa, url=request.host)
        return empresa
    return None

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
    return Presentacion(id, modalidad_presentacion, animacion, videojuegos, disenio, ingenieria)


def registrarSpeedMeeting(id):
    print("numero de sesiones = " + str(request.form["numero_sesiones"]))

    # preguntas = form["preguntas"]
    speed_meeting = Speed_meeting(id)
    for i in range(int(request.form["numero_sesiones"])):
        modalidad_speed_meeting = request.form["modalidad_speed_meeting_" + str(i)] == "presencial"
        descripcion_speed_meeting = request.form["descripcion_speed_meeting_" + str(i)]
        fecha_speed_meeting = request.form["fecha_speed_meeting_" + str(i)]
        fecha_speed_meeting = datetime.strptime(fecha_speed_meeting, "%Y-%m-%d")
        print(fecha_speed_meeting)
        duracion = request.form["duracion_" + str(i)]
        print(duracion)
        speed_meeting.sesiones.append(
            Sesion(id, modalidad_speed_meeting, descripcion_speed_meeting, fecha_speed_meeting, duracion))
    return speed_meeting


def registrarCharla(id):
    modalidad_charlas = request.form["modalidad_charlas"] == "presencial"
    descripcion = request.form["descripcion_charla"]
    fecha_charla = request.form["fecha_charla"]
    hora_charla = request.form["hora_charla"]
    fecha_hora_charla = datetime.strptime(fecha_charla + " " + hora_charla, "%Y-%m-%d %H:%M")
    # ponente = request.form["ponente"]
    return Charla(id, descripcion, modalidad_charlas, fecha_hora_charla, "ponente")

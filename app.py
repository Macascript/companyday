import os
from flask import Flask, render_template, request, redirect
from extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
import json

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
    empresas = Empresa.query.all()
    paises = Pais.query.all()
    if request.method == "POST":
        if Empresa.query.filter_by(email=request.form["email"]).count() > 0:
            return render_template("nuevoIndex.html",state="EmailExists",empresas=empresas,paises=paises)
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
    return render_template("nuevoIndex.html",state="NotLogged",empresas=empresas,paises=paises)

@app.route("/profile", methods=["GET","POST"])
def profile():
    #empresa = Empresa.query.get(request.form["id"])
    return redirect("/")

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
#from crypt import methods
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = "static/logos"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:companyday@macascript.com/companyday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELS

class Actividad(db.Model):
    __tablename__ = "actividad"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(25))


participa = db.Table(
    "participa",
    db.Column("empresa_id",db.Integer,db.ForeignKey("empresa.id")),
    db.Column("actividad_id",db.Integer,db.ForeignKey("actividad.id"))
)

class Empresa(db.Model):
    __tablename__ = "empresa"
    # TODO: resto de atributos de una empresa en la BD
    id = db.Column(db.Integer, primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(100))
    nombre_persona_contacto = db.Column(db.String(100))
    email = db.Column(db.String(320))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion_id = db.Column(db.Integer,db.ForeignKey("poblacion.id"))
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    consentimiento_uso_nombre = db.Column(db.Boolean)
    buscando_candidatos = db.Column(db.Boolean)

    poblacion = db.relationship("Poblacion",uselist=False)
    asistentes = db.relationship("Asistente")
    actividades = db.relationship("Actividad",secondary = participa,backref = "participa")
    presentacion = db.relationship("Presentacion",uselist=False)
    speed_meeting = db.relationship("Speed_meeting",uselist=False)
    charla = db.relationship("Charla",uselist=False)
#
    def __init__(self, nombre, nombre_persona_contacto, email, telefono, direccion, poblacion, codigo_postal, web, logo_url, consentimiento_uso_nombre, buscando_candidatos):
        self.nombre = nombre
        self.nombre_persona_contacto = nombre_persona_contacto
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.poblacion = poblacion
        self.codigo_postal = codigo_postal
        self.web = web
        self.logo_url = logo_url
        self.consentimiento_uso_nombre = consentimiento_uso_nombre
        self.buscando_candidatos = buscando_candidatos

class Pais(db.Model):
    __tablename__ = "pais"
    id = db.Column(db.Integer, primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(50))

    provincias = db.relationship("Provincia")

class Provincia(db.Model):
    __tablename__ = "provincia"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(50))

    poblaciones = db.relationship("Poblacion")

class Poblacion(db.Model):
    __tablename__ = "poblacion"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    provincia_id = db.Column(db.Integer,db.ForeignKey("provincia.id"),primary_key = True)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(100))


class Asistente(db.Model):
    __tablename__ = "asistente"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"))
    nombre_completo = db.Column(db.String(250))
    cargo = db.Column(db.String(100))

    def __init__(self,empresa_id,nombre_completo,cargo):
        self.empresa_id = empresa_id
        self.nombre_completo = nombre_completo
        self.cargo = cargo

class Presentacion(db.Model):
    __tablename__ = "presentacion"
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
    presencial = db.Column(db.Boolean)
    animacion = db.Column(db.Boolean)
    videojuegos = db.Column(db.Boolean)
    disenio = db.Column(db.Boolean)
    ingenieria = db.Column(db.Boolean)

    def __init__(self,empresa_id,presencial,animacion,videojuegos,disenio,ingenieria):
        self.empresa_id = empresa_id
        self.presencial = presencial
        self.animacion = animacion
        self.videojuegos = videojuegos
        self.disenio = disenio
        self.ingenieria = ingenieria

class Sesion(db.Model):
    __tablename__ = "sesion"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    empresa_id = db.Column(db.Integer,db.ForeignKey("speed_meeting.empresa_id"))
    presencial = db.Column(db.Boolean)
    descripcion = db.Column(db.String(500))
    fecha = db.Column(db.Date)
    duracion = db.Column(db.String(2))

    def __init__(self,empresa_id,presencial,descripcion,fecha,duracion):
        self.empresa_id = empresa_id
        self.presencial = presencial
        self.descripcion = descripcion
        self.fecha = fecha
        self.duracion = duracion

# class Speed_meeting(db.Model):
#     __tablename__ = "speed_meeting"
#     empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
#     presencial = db.Column(db.Boolean)
#     descripcion = db.Column(db.String(500))
#     preguntas = db.Column(db.String(500))

#     sesiones = db.relationship("Sesion")

#     def __init__(self,empresa_id,presencial,descripcion,preguntas):
#         self.empresa_id = empresa_id
#         self.presencial = presencial
#         self.descripcion = descripcion
#         self.preguntas = preguntas

class Speed_meeting(db.Model):
    __tablename__ = "speed_meeting"
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
    sesiones = db.relationship("Sesion")

    def __init__(self,empresa_id):
        self.empresa_id = empresa_id

class Charla(db.Model):
    __tablename__ = "charla"
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
    descripcion = db.Column(db.String(500))
    presencial = db.Column(db.Boolean)
    fecha = db.Column(db.DateTime)
    ponente = db.Column(db.String(100))

    def __init__(self,empresa_id,descripcion,presencial,fecha,ponente):
        self.empresa_id = empresa_id
        self.descripcion = descripcion
        self.presencial = presencial
        self.fecha = fecha
        self.ponente = ponente

# END MODELS



# CONTROLLER

@app.route("/plantilla")
def plantilla():
    return render_template("index.html")

@app.route("/user/getempresas")
def getEmpresas():
    lista = []
    for empresa in Empresa.query.all():
        lista.append({
            "id": empresa.id,
            "nombre": empresa.nombre,
            "web": empresa.web,
            "logo_url": empresa.logo_url
        })
    print(lista)
    # body = {
    #     "empresas": lista
    # }
    # return {
    #     'statusCode': 200,
    #     'headers': { 'Access-Control-Allow-Origin' : '*' },
    #     'body' : body
    # }
    return {"empresas": lista}

@app.route("/user/getpaises")
def getPaises():
    lista = []
    for pais in Pais.query.all():
        lista.append({
            "id": pais.id,
            "nombre": pais.nombre,
            "provincias": [{
                "id": provincia.id,
                "nombre": provincia.nombre,
                "poblaciones": [{
                    "id": poblacion.id,
                    "nombre": poblacion.nombre
                } for poblacion in provincia.poblaciones]
            } for provincia in pais.provincias]
        })
    # body = {
    #     "paises": lista
    # }
    # return {
    #     'statusCode': 200,
    #     'headers': { 'Access-Control-Allow-Origin' : '*' },
    #     'body' : body
    # }
    return {"paises": lista}

@app.route("/", methods=["GET","POST"])
def index():
    db.create_all()
    empresas = Empresa.query.all()
    paises = Pais.query.all()
    if request.method == "POST":
        if Empresa.query.filter_by(email=request.form["email"]).count() > 0:
            return render_template("nuevoIndex.html",state="EmailExists")
        new_empresa = registrarEmpresa(request.form,request.files)
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
    
    return redirect("/")

def registrarEmpresa(form,files):
    nombre = form["nombre"]
    print(nombre)
    nombre_persona_contacto = form["nombre_persona_contacto"]
    print(nombre_persona_contacto)
    email = form["email"]
    print(email)
    telefono = form["telefono"]
    print(telefono)
    direccion = form["direccion"]
    print(direccion)
    poblacion = Poblacion.query.filter_by(
        nombre = form["poblacion"],
        provincia_id = Provincia.query.filter_by(
            nombre = form["provincia"],
            pais_id = Pais.query.filter_by(
                nombre = form["pais"]
            ).first().id
        ).first().id
    ).first()
    print(poblacion)
    codigo_postal = form["codigo_postal"]
    print(codigo_postal)
    web = form["web"]
    print(web)
    logo_url = ""
    print("logo_url" in files)
    # check if the post request has the file part
    if 'logo_url' in files:
        file = files['logo_url']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logo_url = UPLOAD_FOLDER+"/"+filename


    consentimiento_uso_nombre = form["consentimiento_uso_nombre"] == "si"
    print(consentimiento_uso_nombre)
    buscando_candidatos = form["buscando_candidatos"] == "si"
    print(buscando_candidatos)
    return Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,logo_url,consentimiento_uso_nombre,buscando_candidatos)

def registrarPresentacion(form,id):
    modalidad_presentacion = form["modalidad_presentacion"] == "presencial"
    print(modalidad_presentacion)
    animacion = "animacion" in form
    print(animacion)
    videojuegos = "videojuegos" in form
    print(videojuegos)
    disenio = "disenio" in form
    print(disenio)
    ingenieria = "ingenieria" in form
    print(ingenieria)
    return Presentacion(id,modalidad_presentacion,animacion,videojuegos,disenio,ingenieria)

def registrarSpeedMeeting(form,id):
    print("numero de sesiones = "+str(form["numero_sesiones"]))
    
    # preguntas = form["preguntas"]
    speed_meeting = Speed_meeting(id)
    for i in range(int(form["numero_sesiones"])):
        modalidad_speed_meeting = form["modalidad_speed_meeting_"+str(i)] == "presencial"
        descripcion_speed_meeting = form["descripcion_speed_meeting_"+str(i)]
        fecha_speed_meeting = form["fecha_speed_meeting_"+str(i)]
        fecha_speed_meeting = datetime.strptime(fecha_speed_meeting,"%Y-%m-%d")
        print(fecha_speed_meeting)
        duracion = form["duracion_"+str(i)]
        print(duracion)
        speed_meeting.sesiones.append(Sesion(id,modalidad_speed_meeting,descripcion_speed_meeting,fecha_speed_meeting,duracion))
    return speed_meeting

def registrarCharla(form,id):
    modalidad_charlas = form["modalidad_charlas"] == "presencial"
    descripcion = form["descripcion_charla"]
    fecha_charla = form["fecha_charla"]
    hora_charla = form["hora_charla"]
    fecha_hora_charla = datetime.strptime(fecha_charla+" "+hora_charla,"%Y-%m-%d %H:%M")
    # ponente = request.form["ponente"]
    return Charla(id,descripcion,modalidad_charlas,fecha_hora_charla,"ponente")

@app.route("/prueba", methods=["GET","POST"])
def prueba():
    return render_template("prueba.html",paises=Pais.query.all())

@app.route("/prueba2", methods=["GET","POST"])
def prueba2():
    print("here we go again")
    # check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logo_url = UPLOAD_FOLDER+"/"+filename
            return "<img src='"+UPLOAD_FOLDER+"/"+filename+"'>"
    return "VAYA"




if __name__ == '__main__':
    app.run(port=5000,debug=True)

# END CONTROLLER END
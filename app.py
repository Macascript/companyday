#from crypt import methods
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/logos"
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
    fecha = db.Column(db.Date)
    duracion = db.Column(db.String(2))

    def __init__(self,empresa_id,fecha,duracion):
        self.empresa_id = empresa_id
        self.fecha = fecha
        self.duracion = duracion

class Speed_meeting(db.Model):
    __tablename__ = "speed_meeting"
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
    presencial = db.Column(db.Boolean)
    descripcion = db.Column(db.String(500))
    preguntas = db.Column(db.String(500))

    sesiones = db.relationship("Sesion")

    def __init__(self,empresa_id,presencial,descripcion,preguntas):
        self.empresa_id = empresa_id
        self.presencial = presencial
        self.descripcion = descripcion
        self.preguntas = preguntas

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

@app.route("/", methods=["GET","POST"])
def index():
    empresas = Empresa.query.all()
    paises = Pais.query.all()
    db.create_all()
    return render_template("nuevoIndex.html",empresas=empresas)

@app.route("/registered", methods=["GET","POST"])
def profile():
    if request.method == "POST":
        # TODO: distintos parametros que recibe del formulario
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
            nombre == request.form["poblacion"],
            provincia_id == Provincia.query.filter_by(
                nombre == request.form["provincia"],
                pais_id == Pais.query.filter_by(
                    nombre == request.form["pais"]
                ).first().id
            ).first().id
        ).first()
        print(poblacion)
        codigo_postal = request.form["codigo_postal"]
        print(codigo_postal)
        web = request.form["web"]
        print(web)

        # check if the post request has the file part
        # if 'file' in request.files:
        #     file = request.files['file']
        #     # if user does not select file, browser also
        #     # submit a empty part without filename
        #     if file.filename != '':
        #         if file and allowed_file(file.filename):
        #             filename = secure_filename(file.filename)
        #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #             logo_url = UPLOAD_FOLDER+"/"+filename

        consentimiento_uso_nombre = request.form["consentimiento_uso_nombre"] == "si"
        print(consentimiento_uso_nombre)
        buscando_candidatos = request.form["buscando_candidatos"] == "si"
        print(buscando_candidatos)
        poblacion = Poblacion.query.get((1,1,1))
        print(poblacion)
        new_empresa = Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,"logo_url",consentimiento_uso_nombre,buscando_candidatos)
        db.session.add(new_empresa)
        print(new_empresa)

        if "feria_empresas" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["feria_empresas"])))
        if "presentacion" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["presentacion"])))
        if "speed_meetings" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["speed_meetings"])))
        if "charlas" in request.form:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["charlas"])))

        print(new_empresa.actividades)

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
        presentacion = Presentacion(new_empresa.id,modalidad_presentacion,animacion,videojuegos,disenio,ingenieria)
        db.session.add(presentacion)
        new_empresa.presentacion = presentacion
        print(new_empresa.presentacion)

        modalidad_speed_meeting = request.form["modalidad_speed_meeting"] == "presencial"
        fecha_speed_meeting = request.form["fecha_speed_meeting"]
        fecha_speed_meeting = datetime.strptime(fecha_speed_meeting,"%Y-%m-%d")
        print(fecha_speed_meeting)
        duracion = request.form["duracion"]
        print(duracion)
        descripcion = request.form["descripcion_speed_meeting"]
        print(descripcion)
        # preguntas = request.form["preguntas"]
        speed_meeting = Speed_meeting(new_empresa.id,modalidad_speed_meeting,descripcion,"preguntas")
        db.session.add(speed_meeting)
        new_empresa.speed_meeting = speed_meeting
        print(new_empresa.speed_meeting)
        sesion = Sesion(new_empresa,fecha_speed_meeting,duracion)
        db.session.add(sesion)
        new_empresa.speed_meeting.sesiones.append(sesion)
        print(new_empresa.speed_meeting.sesiones)

        modalidad_charlas = request.form["modalidad_charlas"] == "presencial"
        descripcion = request.form["descripcion_charla"]
        fecha_charla = request.form["fecha_charla"]
        hora_charla = request.form["hora_charla"]
        fecha_hora_charla = datetime.strptime(fecha_charla+" "+hora_charla,"%Y-%m-%d %H:%M")
        # ponente = request.form["ponente"]
        charla = Charla(new_empresa.id,descripcion,modalidad_charlas,fecha_hora_charla,"ponente")
        db.session.add(charla)
        new_empresa.charla = charla
        
        db.session.commit()
    return redirect("/")

@app.route("/prueba")
def prueba():
    return render_template("prueba.html",paises=Pais.query.all())

@app.route("/prueba2")
def prueba2():
    print(request.args.get("msg") is None)
    return "Hola"




if __name__ == '__main__':
    app.run(port=5000,debug=True)

# END CONTROLLER
#from crypt import methods
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from pendulum import date

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
    poblacion = db.Column(db.Integer,db.ForeignKey("poblacion.id"))
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    consentimiento_uso_nombre = db.Column(db.Boolean)
    buscando_candidatos = db.Column(db.Boolean)

    asistentes = db.relationship("asistente")
    actividades = db.relationship("actividad",secondary = participa,backref = "participa")
    presentacion = db.relationship("presentacion")
    speed_meeting = db.relationship("speed_meeting")
    charla = db.relationship("charla")

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

    sesiones = db.relationship("sesion")

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

@app.route("/", methods=["GET","POST"])
def index():
    # empresas = Empresa.query.all()
    # return render_template("index.html",empresas=empresas)
    # db.create_all()
    return render_template("nuevoIndex.html")

@app.route("/registered", methods=["GET","POST"])
def profile():
    if request.method == "POST":
        # TODO: distintos parametros que recibe del formulario
        nombre = request.form["nombre"]
        nombre_persona_contacto = request.form["nombre_persona_contacto"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        poblacion = request.form["poblacion"]
        codigo_postal = request.form["codigo_postal"]
        web = request.form["web"]
        logo_url = request.form["logo_url"]
        consentimiento_uso_nombre = request.form["consentimiento_uso_nombre"]
        buscando_candidatos = request.form["buscando_candidatos"]
        new_empresa = Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,logo_url,consentimiento_uso_nombre,buscando_candidatos)

        if request.form["feria_empresas"] is not None:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["feria_empresas"])))
        if request.form["presentacion"] is not None:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["presentacion"])))
        if request.form["speed_meetings"] is not None:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["speed_meetings"])))
        if request.form["charlas"] is not None:
            new_empresa.actividades.append(Actividad.query.get(int(request.form["charlas"])))

        modalidad_presentacion = request.form["modalidad_presentacion"] is not None
        animacion = request.form["animacion"] is not None
        videojuegos = request.form["videojuegos"] is not None
        disenio = request.form["disenio"] is not None
        ingenieria = request.form["ingenieria"] is not None
        new_empresa.presentacion = Presentacion(new_empresa.id,modalidad_presentacion,animacion,videojuegos,disenio,ingenieria)

        modalidad_speed_meeting = request.form["modalidad_speed_meeting"] is not None
        fecha_speed_meeting = request.form["fecha_speed_meeting"]
        fecha_speed_meeting = datetime.strptime(fecha_speed_meeting,"%d/%m/%Y")
        duracion = request.form["duracion"]
        descripcion = request.form["descripcion"]
        preguntas = request.form["preguntas"]
        new_empresa.speed_meeting = Speed_meeting(new_empresa.id,modalidad_speed_meeting,descripcion,preguntas)
        new_empresa.speed_meeting.sesiones.append(Sesion(new_empresa,fecha_speed_meeting,duracion))

        modalidad_charlas = request.form["modalidad_charlas"] is not None
        descripcion = request.form["descripcion"]
        fecha_charla = request.form["fecha_charla"]
        hora_charla = request.form["hora_charla"]
        fecha_hora_charla = datetime.strptime(fecha_charla+"-"+hora_charla,"%d/%m/%Y-%H:%M")
        ponente = request.form["ponente"]
        new_empresa.charla = Charla(new_empresa.id,descripcion,modalidad_charlas,fecha_hora_charla,ponente)

        db.session.add(new_empresa)
        db.session.commit()

@app.route("/prueba")
def prueba():
    return """
        <form action="/prueba2" type="GET">
            <input type="checkbox" name="msg" value="hola"/>
            <input type="checkbox" name="msg" value="mundo"/>
            <input type="submit"/>
        </form>

    """

@app.route("/prueba2")
def prueba2():
    print(request.args.get("msg") is None)
    return "Hola"




if __name__ == '__main__':
    app.run(port=5000,debug=True)

# END CONTROLLER
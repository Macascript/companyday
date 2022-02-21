#from crypt import methods
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:companyday@macascript.com/companyday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELS
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
    buscando_candidatos = db.Column(db.Boolean)

    asistentes = db.relationship("asistente")
    actividades = db.relationship("actividad",secondary = participa,backref = "participa")

    def __init__(self, nombre, nombre_persona_contacto, email, telefono, direccion, poblacion, codigo_postal, web, logo_url, buscando_candidatos):
        self.nombre = nombre
        self.nombre_persona_contacto = nombre_persona_contacto
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.poblacion = poblacion
        self.codigo_postal = codigo_postal
        self.web = web
        self.logo_url = logo_url
        self.buscando_candidatos = buscando_candidatos

class Pais(db.Model):
    __tablename__ = "pais"
    id = db.Column(db.Integer, primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(50))
    provincias = db.relationship("Provincia")

class Provincia(db.Model):
    __tablename__ = "provincia"
    id = db.Column(db.Integer)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(50))

class Poblacion(db.Model):
    __tablename__ = "poblacion"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    provincia_id = db.Column(db.Integer,db.ForeignKey("provincia.id"),primary_key = True)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(100))

class Actividad(db.Model):
    __tablename__ = "actividad"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(25))

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
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"))
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

    def __init__(self,empresa_id,presencial,descripcion,preguntas):
        self.empresa_id = empresa_id
        self.presencial = presencial
        self.descripcion = descripcion
        self.preguntas = preguntas

class Charla(db.Model):
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
        buscando_candidatos = request.form["buscando_candidatos"]
        new_empresa = Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,logo_url,buscando_candidatos)
        # db.session.add(new_empresa)
        # db.session.commit()

if __name__ == '__main__':
    app.run(port=5000,debug=True)

# END CONTROLLER
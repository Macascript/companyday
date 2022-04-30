import json

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from init import get_app

db = None


def init_db(app):
    global db
    if db == None:
        db = SQLAlchemy()  # class db extends app
    return db


def get_db():
    global db
    if db == None:
        app = get_app()
        db = init_db(app)
    return db

app = get_app()
db = init_db(app)


class Actividad(db.Model):
    __tablename__ = "actividad"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(25))


class Asistente(db.Model):
    __tablename__ = "asistente"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    nombre_completo = db.Column(db.String(250))
    cargo = db.Column(db.String(100))


class Charla(db.Model):
    __tablename__ = "charla"
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), primary_key=True)
    descripcion = db.Column(db.String(500))
    presencial = db.Column(db.Boolean)
    fecha = db.Column(db.DateTime)
    ponente = db.Column(db.String(100))


participa = db.Table(
    "participa",
    db.Column("empresa_id", db.Integer, db.ForeignKey("empresa.id")),
    db.Column("actividad_id", db.Integer, db.ForeignKey("actividad.id"))
)


class Empresa(UserMixin, db.Model):
    __tablename__ = "empresa"
    # TODO: resto de atributos de una empresa en la BD
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    nombre_persona_contacto = db.Column(db.String(100))
    email = db.Column(db.String(320))
    contrasenya = db.Column(db.String(16))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion_id = db.Column(db.Integer, db.ForeignKey("poblacion.id"))
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    consentimiento_uso_nombre = db.Column(db.Boolean)
    buscando_candidatos = db.Column(db.Boolean)
    esta_confirmado = db.Column(db.Boolean, default=False)
    esta_creado_jb = db.Column(db.Boolean, default=False)
    esta_actualizado_jb = db.Column(db.Boolean, default=False)
    user_hash = db.Column(db.String(50))
    usertype = db.Column(db.Integer) # 1: Admin, 2: User

    poblacion = db.relationship("Poblacion", uselist=False)
    asistentes = db.relationship("Asistente")
    actividades = db.relationship("Actividad", secondary=participa, backref="participa")
    presentacion = db.relationship("Presentacion", uselist=False)
    speed_meeting = db.relationship("Speed_meeting", uselist=False)
    charla = db.relationship("Charla", uselist=False)
    


class Pais(db.Model):
    __tablename__ = "pais"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))

    provincias = db.relationship("Provincia")


class Poblacion(db.Model):
    __tablename__ = "poblacion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provincia_id = db.Column(db.Integer, db.ForeignKey("provincia.id"), primary_key=True)
    pais_id = db.Column(db.Integer, db.ForeignKey("pais.id"), primary_key=True)
    nombre = db.Column(db.String(100))

    provincia = db.relationship("Provincia", uselist=False)


class Presentacion(db.Model):
    __tablename__ = "presentacion"
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), primary_key=True)
    presencial = db.Column(db.Boolean)
    animacion = db.Column(db.Boolean)
    videojuegos = db.Column(db.Boolean)
    disenio = db.Column(db.Boolean)
    ingenieria = db.Column(db.Boolean)


class Provincia(db.Model):
    __tablename__ = "provincia"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pais_id = db.Column(db.Integer, db.ForeignKey("pais.id"), primary_key=True)
    nombre = db.Column(db.String(50))

    poblaciones = db.relationship("Poblacion")
    pais = db.relationship("Pais", uselist=False)


class Sesion(db.Model):
    __tablename__ = "sesion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("speed_meeting.empresa_id"))
    presencial = db.Column(db.Boolean)
    descripcion = db.Column(db.String(500))
    fecha = db.Column(db.Date)
    duracion = db.Column(db.String(2))


class Speed_meeting(db.Model):
    __tablename__ = "speed_meeting"
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), primary_key=True)
    sesiones = db.relationship("Sesion")

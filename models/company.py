from app import db

class Company(db.Model):
    # TODO: resto de atributos de una empresa en la BD
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    nombre_persona_contacto = db.Column(db.String(100))
    email = db.Column(db.String(320))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion = db.Column(db.Integer)
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    buscando_candidatos = db.Column(db.Bool)
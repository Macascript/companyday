from app import db

class Empresa(db.Model):
    # TODO: resto de atributos de una empresa en la BD
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    nombre_persona_contacto = db.Column(db.String(100))
    email = db.Column(db.String(320))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion = db.Column(db.Integer)
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    buscando_candidatos = db.Column(db.Bool)

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
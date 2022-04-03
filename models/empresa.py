from extensions import db

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
    contrasenya = db.Column(db.String(16))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion_id = db.Column(db.Integer,db.ForeignKey("poblacion.id"))
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    consentimiento_uso_nombre = db.Column(db.Boolean)
    buscando_candidatos = db.Column(db.Boolean)
    es_creado = db.Column(db.Boolean)
    es_verificado = db.Column(db.Boolean)
    es_actualizado = db.Column(db.Boolean)

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
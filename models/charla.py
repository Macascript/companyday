from extensions import db

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
from extensions import db

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
from extensions import db

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
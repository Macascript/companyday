from extensions import db

class Actividad(db.Model):
    __tablename__ = "actividad"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(25))
from extensions import db

class Provincia(db.Model):
    __tablename__ = "provincia"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(50))

    poblaciones = db.relationship("Poblacion")
    pais = db.relationship("Pais", uselist = False)
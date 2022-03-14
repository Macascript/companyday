from extensions import db

class Poblacion(db.Model):
    __tablename__ = "poblacion"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    provincia_id = db.Column(db.Integer,db.ForeignKey("provincia.id"),primary_key = True)
    pais_id = db.Column(db.Integer,db.ForeignKey("pais.id"),primary_key = True)
    nombre = db.Column(db.String(100))

    provincia = db.relationship("Provincia", uselist = False)
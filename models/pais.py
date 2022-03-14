from extensions import db

class Pais(db.Model):
    __tablename__ = "pais"
    id = db.Column(db.Integer, primary_key = True,autoincrement = True)
    nombre = db.Column(db.String(50))

    provincias = db.relationship("Provincia")
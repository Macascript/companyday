from extensions import db

class Asistente(db.Model):
    __tablename__ = "asistente"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"))
    nombre_completo = db.Column(db.String(250))
    cargo = db.Column(db.String(100))

    def __init__(self,empresa_id,nombre_completo,cargo):
        self.empresa_id = empresa_id
        self.nombre_completo = nombre_completo
        self.cargo = cargo
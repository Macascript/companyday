from extensions import db

class Speed_meeting(db.Model):
    __tablename__ = "speed_meeting"
    empresa_id = db.Column(db.Integer,db.ForeignKey("empresa.id"),primary_key = True)
    sesiones = db.relationship("Sesion")

    def __init__(self,empresa_id):
        self.empresa_id = empresa_id
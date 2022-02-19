from crypt import methods
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:companyday@macascript.com/companyday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Empresa(db.Model):
    # TODO: resto de atributos de una empresa en la BD
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    nombre_persona_contacto = db.Column(db.String(100))
    email = db.Column(db.String(320))
    telefono = db.Column(db.String(13))
    direccion = db.Column(db.String(500))
    poblacion = db.Column(db.Integer)
    codigo_postal = db.Column(db.String(10))
    web = db.Column(db.String(500))
    logo_url = db.Column(db.String(200))
    buscando_candidatos = db.Column(db.Boolean)

    def __init__(self, nombre, nombre_persona_contacto, email, telefono, direccion, poblacion, codigo_postal, web, logo_url, buscando_candidatos):
        self.nombre = nombre
        self.nombre_persona_contacto = nombre_persona_contacto
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.poblacion = poblacion
        self.codigo_postal = codigo_postal
        self.web = web
        self.logo_url = logo_url
        self.buscando_candidatos = buscando_candidatos

@app.route("/", methods=["GET","POST"])
def index():
    empresas = Empresa.query.all()
    return render_template("index.html",empresas=empresas)

@app.route("/registered", methods=["GET","POST"])
def profile():
    if request.method == "POST":
        # TODO: distintos parámetros que recibe del formulario
        nombre = request.form["nombre"]
        nombre_persona_contacto = request.form["nombre_persona_contacto"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        poblacion = request.form["poblacion"]
        codigo_postal = request.form["codigo_postal"]
        web = request.form["web"]
        logo_url = request.form["logo_url"]
        buscando_candidatos = request.form["buscando_candidatos"]
        new_empresa = Empresa(nombre,nombre_persona_contacto,email,telefono,direccion,poblacion,codigo_postal,web,logo_url,buscando_candidatos)
        db.session.add(new_empresa)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5000,debug=True)
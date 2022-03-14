import flask
from flask import request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename


from models.empresa import Empresa
from models.poblacion import Poblacion
from extensions import db

from extensions import UPLOAD_FOLDER

empresa_rutas = flask.Blueprint("empresa_rutas",__name__)

@empresa_rutas.route("/profile",methods=["GET","POST"])
def profile():
    if request.method == "POST":
        empresa = Empresa.query.filter_by(email=request.form["email"],contrasenya=request.form["contrasenya"]).one_or_none()
        if empresa is not None:
            return render_template(url_for("profile",empresa = empresa))
    return redirect(url_for("/",state = "FailedLogging"))

@empresa_rutas.route("/changedata",methods=["GET","POST"])
def changedata():
    f = request.form
    id = f["id"]
    empresa = Empresa.query.get(id)
    if "nombre" in f:
        empresa.nombre = f["nombre"]
    if "nombre_persona_contacto" in f:
        empresa.nombre_persona_contacto = f["nombre_persona_contacto"]
    if "telefono" in f:
        empresa.telefono = f["telefono"]
    if "direccion" in f:
        empresa.direccion = f["direccion"]
    if "poblacion" in f:
        empresa.poblacion = Poblacion.query.get(f["poblacion"])
    if "codigo_postal" in f:
        empresa.codigo_postal = f["codigo_postal"]
    if "web" in f:
        empresa.web = f["web"]
    if "logo_url" in request.files:
        file = request.files['logo_url']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename != '':
            os.remove(empresa.logo_url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            empresa.logo_url = UPLOAD_FOLDER+"/"+filename
    if "consentimiento_uso_nombre" in f:
        empresa.consentimiento_uso_nombre = f["consentimiento_uso_nombre"]
    if "buscando_candidatos" in f:
        empresa.buscando_candidatos = f["buscando_candidatos"]

    db.session.commit()
    return redirect("/prueba")
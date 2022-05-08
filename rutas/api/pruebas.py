import flask
from flask import render_template, request
from werkzeug.utils import secure_filename
import os
from models import Empresa

from models import Pais

UPLOAD_FOLDER = "static/logos"

pruebas = flask.Blueprint("pruebas",__name__)

@pruebas.route("/prueba", methods=["GET","POST"])
def prueba():
    return render_template("prueba.html", paises=Pais.query.all())

@pruebas.route("/prueba2", methods=["GET","POST"])
def prueba2():
    print("here we go again")
    # check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return "<img src='"+UPLOAD_FOLDER+"/"+filename+"'>"
    return "VAYA"

@pruebas.route("/pruebapedro")
def pruebapedro():
    return render_template("utad.html", empresas=Empresa.query.all())

@pruebas.route("/pruebamaca")
def pruebamaca():
    # <meta id="paises" data-paises="{{ paises|tojson }}">
	# <meta id="empresas" data-empresas="{{ empresas|tojson }}">
    return render_template("nuevoIndexVue.html")

@pruebas.route("/pruebamaca2")
def pruebamaca2():
    return render_template("editarPerfilVue.html")

@pruebas.route("/primeraruta")
def primeraruta():
    return render_template("plantilla_home.html")

@pruebas.route("/segundaruta")
def segundaruta():
    return render_template("carrusel_actividades_alumnos.html")

@pruebas.route("/terceraruta")
def terceraruta():
    return render_template("footer.html")
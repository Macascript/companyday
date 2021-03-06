import flask
from flask import jsonify

from models import Empresa
#from api_functions import empresa_data
from rutas.api.api_functions import empresa_data

uni_api = flask.Blueprint("uni_api", __name__)

@uni_api.route("/admin/getempresa/<id>")
def getEmpresa(id):
    return empresa_data(id)

@uni_api.route("/admin/getempresas")
def getEmpresasExtended():
    lista = []
    for empresa in Empresa.query.all():
        lista.append({
            "id": empresa.id,
            "nombre": empresa.nombre,
            "nombre_persona_contacto": empresa.nombre_persona_contacto,
            "email": empresa.email,
            "telefono": empresa.telefono,
            "direccion": empresa.direccion,
            "poblacion": empresa.poblacion.nombre,
            "provincia": empresa.poblacion.provincia.nombre,
            "pais": empresa.poblacion.provincia.pais.nombre,
            "codigo_postal": empresa.codigo_postal,
            "web": empresa.web,
            "logo_url": empresa.logo_url,
            "consentimiento_uso_nombre": empresa.consentimiento_uso_nombre,
            "buscando_candidatos": empresa.buscando_candidatos
        })
    print(lista)
    # body = {
    #     "empresas": lista
    # }
    # return {
    #     'statusCode': 200,
    #     'headers': { 'Access-Control-Allow-Origin' : '*' },
    #     'body' : body
    # }
    return jsonify({"empresas": lista})
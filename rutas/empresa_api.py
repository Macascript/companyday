import flask
from flask import jsonify
from itsdangerous import json

from models.empresa import Empresa
from models.pais import Pais

empresa_api = flask.Blueprint("empresa_api",__name__)

# Consultas

@empresa_api.route("/user/getempresas")
def getEmpresas():
    lista = []
    for empresa in Empresa.query.all():
        lista.append({
            "id": empresa.id,
            "nombre": empresa.nombre,
            "web": empresa.web,
            "logo_url": empresa.logo_url
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
    # return jsonify({"empresas": lista})
    return "Hola"

@empresa_api.route("/user/getpaises")
def getPaises():
    lista = []
    for pais in Pais.query.all():
        lista.append({
            "id": pais.id,
            "nombre": pais.nombre,
            "provincias": [{
                "id": provincia.id,
                "nombrePais": pais.nombre,
                "nombre": provincia.nombre,
                "poblaciones": [{
                    "id": poblacion.id,
                    "nombreProvincia": provincia.nombre,
                    "nombrePais": pais.nombre,
                    "nombre": poblacion.nombre
                } for poblacion in provincia.poblaciones]
            } for provincia in pais.provincias]
        })
    # body = {
    #     "paises": lista
    # }
    # return {
    #     'statusCode': 200,
    #     'headers': { 'Access-Control-Allow-Origin' : '*' },
    #     'body' : body
    # }
    print(lista)
    return jsonify({"paises": lista})

# Funciones
from flask import jsonify

from models import Empresa

def empresa_data(empresa):
    if empresa is not None:
        return jsonify({
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body' : {
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
            }
        })
    else:
        return jsonify({
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body' : "ups"
        })
import flask
from flask import jsonify

from flask_login import current_user

session_handler = flask.Blueprint("session_handler", __name__)

@session_handler.route("/session/status", methods=["GET"])
def status():
    if current_user.is_authenticated:
        return jsonify({"Nombre Empresa" : current_user.nombre, "ID:" : current_user.id})
    return "Necesitas estar logeado para poder acceder a tu sesion"
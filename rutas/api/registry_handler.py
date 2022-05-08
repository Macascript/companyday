import flask
from flask import jsonify

from models import Empresa, db

registry_handler = flask.Blueprint("registry_handler", __name__)

@registry_handler.route('/registry/confirm/<empresa_id>/<userhash>/', methods=['GET'])
def confirmuser(empresa_id, userhash):
    empresa = Empresa.query.filter_by(id = empresa_id).first()
    if not empresa:
        response ='Invalid url.'
    elif userhash != empresa.user_hash:
        response ='Invalid url.'
    elif empresa.esta_verificado:
        response ='Url already used.'
    else:
        try:
            response = 'User confirmed.'
            empresa.esta_verificado = 1
            db.session.commit()
        except:
            db.session.rollback()
            response = "Error confirming user!"
    return jsonify(response)
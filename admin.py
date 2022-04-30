from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from init import get_app
from models import Empresa, get_db

admin = Admin(get_app())

class UniModelView(ModelView):
    pass

admin.add_view(UniModelView(Empresa,get_db().session))
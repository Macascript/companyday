from locale import currency
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from init import get_app
from models import Empresa, get_db
from flask_login import current_user

class UniIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 3

admin = Admin(get_app(),index_view=UniIndexView())

class UniModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 3



admin.add_view(UniModelView(Empresa,get_db().session))
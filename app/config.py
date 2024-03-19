import os
from .filtros_jinja import configurar_jinja

def configurações(app):
    app.config["SECRET_KEY"] = os.urandom(20).hex()
    configurar_jinja(app)
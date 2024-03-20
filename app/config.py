import os
from .filtros_jinja import configurar_jinja
from flask_caching import Cache

cache = Cache()

def configurações(app):
    app.config["SECRET_KEY"] = os.urandom(20).hex()
    configurar_jinja(app)
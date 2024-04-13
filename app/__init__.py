import os
from pathlib import Path

from flask.app import Flask
from flask_wtf import CSRFProtect

from .ext.cache.cache import cache
from .ext.jinja import registrar_filtros
from .ext.site import configurar_blueprints


def create_app():
    app = Flask(
        __name__,
        static_folder=Path("../static/"),
    )
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    app.config["SECRET_KEY"] = os.getenv("FLASK_KEY")
    CSRFProtect(app)
    configurar_blueprints(app)
    registrar_filtros(app)
    return app

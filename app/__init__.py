import os
from pathlib import Path

from flask.app import Flask
from flask_wtf import CSRFProtect

from .blueprints import configurar_blueprints
from .ext.cache.cache import cache
from .ext.db.db import db
from .ext.jinja import registrar_filtros


def create_app():
    app = Flask(
        __name__,
        static_folder=Path("../static/"),
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DB")
    app.config["SECRET_KEY"] = os.getenv("FLASK_KEY")
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    db.init_app(app)
    CSRFProtect(app)
    configurar_blueprints(app)
    registrar_filtros(app)
    return app

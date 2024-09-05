import os
from pathlib import Path

from flask.app import Flask
from flask_wtf import CSRFProtect

from .bp import register_blueprints
from .ext.bcrypt import bcrypt
from .ext.cache import cache
from .ext.db.db import db
from .ext.jinja.config import jinja_config
from .ext.login import login_manager

caminho_static = Path("../static/")
caminho_templates = Path("../static/templates/")


def create_app() -> Flask:
    """Função que cria o App"""
    app: Flask = Flask(
        __name__, static_folder=caminho_static, template_folder=caminho_templates
    )
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRE_SQL_URL")
    app.config["SECRET_KEY"] = os.getenv("FLASK_KEY")
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app)
    bcrypt.init_app(app)
    app = register_blueprints(app)
    app = jinja_config(app)
    return app

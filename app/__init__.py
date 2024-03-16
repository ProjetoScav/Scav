import os
from app.funcs.auxiliares import formatar_cnpj
from flask.app import Flask
from flask_wtf import CSRFProtect

from .rotas import configure


def create_app():
    app = Flask(
        __name__,
        template_folder="../resources/templates/",
        static_folder="../resources/static/",
    )
    app.config["SECRET_KEY"] = os.urandom(20).hex()
    CSRFProtect(app)
    configure(app)
    app.jinja_env.filters["cnpj_format"] = formatar_cnpj
    return app
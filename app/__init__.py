import os
from app.funcs.auxiliares import formatar_cnpj
from flask.app import Flask
from flask_wtf import CSRFProtect
from flask_caching import Cache
from .rotas import configure
from .blueprints import configure_blueprint 


def create_app():
    app = Flask(
        __name__,
        template_folder="../resources/templates/",
        static_folder="../resources/static/",
    )
    app.config["SECRET_KEY"] = os.urandom(20).hex()
    app.config["CACHE_TYPE"] = "SimpleCache"
    Cache(app)
    CSRFProtect(app)
    configure(app)
    configure_blueprint(app)
    app.jinja_env.filters["cnpj_format"] = formatar_cnpj
    return app
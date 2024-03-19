from flask.app import Flask
from flask_wtf import CSRFProtect
from .rotas import configurar_rotas
from .blueprints import configure_blueprint 
from app.funcionalidades.frontend import cache
from .config import configurações

def create_app():
    app = Flask(
        __name__,
        template_folder="../resources/templates/",
        static_folder="../resources/static/",
    )
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    CSRFProtect(app)
    configurar_rotas(app)
    configurações(app)
    configure_blueprint(app)
    return app
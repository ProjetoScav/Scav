from flask.app import Flask
from flask_wtf import CSRFProtect
from .blueprints import configure_blueprint 
from .config import configurações, cache

def create_app():
    app = Flask(
        __name__,
        static_folder="../static/",
    )
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    CSRFProtect(app)
    configurações(app)
    configure_blueprint(app)
    return app
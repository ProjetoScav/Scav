from flask.app import Flask
from .blueprints import configurar_blueprints
from .config import configurações
from .extensions import cache, configurar_extensões


def create_app():
    app = Flask(
        __name__,
        static_folder="../static/",
    )
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    configurações(app)
    configurar_blueprints(app)
    configurar_extensões(app)
    return app

from flask import Flask

from .cnpj.blueprint import cnpj_blueprint
from .download.blueprint import download_blueprint
from .home.blueprint import home_blueprint


def configurar_blueprints(app: Flask) -> Flask:
    app.register_blueprint(cnpj_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(download_blueprint)
    return app

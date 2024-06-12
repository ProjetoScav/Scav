from flask import Flask

from .cnpj.blueprint import cnpj_blueprint
from .componentes.blueprint import componentes_blueprint
from .download.blueprint import download_blueprint
from .home.blueprint import home_blueprint


def register_blueprints(app: Flask) -> Flask:
    """Função que registra os blueprints com as
    rotas no app e o retorna"""
    app.register_blueprint(cnpj_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(download_blueprint)
    app.register_blueprint(componentes_blueprint)
    return app

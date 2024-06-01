from .cnpj import cnpj_blueprint
from .home import home_blueprint
from .download import download_blueprint


def configurar_blueprints(app):
    app.register_blueprint(cnpj_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(download_blueprint)
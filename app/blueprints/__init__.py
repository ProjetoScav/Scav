from .cnpj import cnpj_blueprint
from .home import home_blueprint
def configure_blueprint(app):
    app.register_blueprint(cnpj_blueprint)
    app.register_blueprint(home_blueprint)
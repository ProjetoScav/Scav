from .cnpj import cnpj_blueprint

def configure_blueprint(app):
    app.register_blueprint(cnpj_blueprint)
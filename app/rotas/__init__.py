from .home import rota_home
from .cnpj import rota_cnpj

def configure(app):
    rota_home(app)
    rota_cnpj(app)
from flask import Blueprint

from .cnpj import cnpj_rota

cnpj_blueprint: Blueprint = Blueprint("cnpj", __name__)
cnpj_blueprint = cnpj_rota(cnpj_blueprint)

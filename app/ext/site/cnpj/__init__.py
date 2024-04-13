from flask import Blueprint
from .cnpj import rota_cnpj

cnpj_blueprint = Blueprint("cnpj", __name__, template_folder="templates")
rota_cnpj(cnpj_blueprint)

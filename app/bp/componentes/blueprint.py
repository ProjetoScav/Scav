from flask import Blueprint

from .componentes import componentes_rotas

componentes_blueprint: Blueprint = Blueprint("componentes", __name__)
componentes_blueprint = componentes_rotas(componentes_blueprint)

from flask import Blueprint

from .componentes import componentes_routes

componentes_blueprint: Blueprint = Blueprint("componentes", __name__)
componentes_blueprint = componentes_routes(componentes_blueprint)

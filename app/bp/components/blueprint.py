from flask import Blueprint

from .components import components_routes

components_blueprint: Blueprint = Blueprint("components", __name__)
components_blueprint = components_routes(components_blueprint)

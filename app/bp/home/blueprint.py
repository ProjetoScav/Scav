from flask import Blueprint

from .home import home_routes

home_blueprint: Blueprint = Blueprint("home", __name__)
home_blueprint = home_routes(home_blueprint)

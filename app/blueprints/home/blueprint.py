from flask import Blueprint

from .home import home_rotas

home_blueprint: Blueprint = Blueprint("home", __name__, template_folder="templates")
home_blueprint = home_rotas(home_blueprint)

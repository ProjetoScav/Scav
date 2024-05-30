from flask import Blueprint

from .home import rota_home

home_blueprint = Blueprint("home", __name__, template_folder="templates")

rota_home(home_blueprint)
from flask import Blueprint

from .login import login_routes

login_blueprint: Blueprint = Blueprint("login", __name__)
login_blueprint = login_routes(login_blueprint)

from flask import Blueprint

from .download import download_rotas

download_blueprint: Blueprint = Blueprint("download", __name__)
download_blueprint = download_rotas(download_blueprint)

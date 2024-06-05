from flask import Blueprint

from .download import download_rotas

download_blueprint: Blueprint = Blueprint(
    "download", __name__, template_folder="templates"
)
download_blueprint = download_rotas(download_blueprint)

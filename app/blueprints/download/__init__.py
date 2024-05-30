from flask import Blueprint
from .download import rota_download

download_blueprint = Blueprint("download", __name__, template_folder="templates")
rota_download(download_blueprint)
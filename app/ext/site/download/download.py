from flask import redirect, request, session, url_for

from app.objetos.requisição import Requisição

from .funcs.email import enviar_email
from .operador import Scav


def rota_download(blueprint):
    @blueprint.route("/download", methods=["POST"])
    def download():
        email = request.get_json()["pay-email"]
        if session.get("_requisição"):
            req = Requisição(**session.get("_requisição"))
        else:
            req = Requisição()
        scav = Scav(req)
        caminho = scav.exportar_os_dados()
        print(caminho)
        enviar_email(email, caminho)
        return redirect(url_for("home.home"))

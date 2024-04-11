from flask import redirect, request, session, url_for

from app.objetos.requisição import Requisição

from .funcs.email import enviar_email
from .operador import Scav


def rota_download(blueprint):
    @blueprint.route("/download", methods=["POST"])
    def download():
        request.get_json()
        email = request.args.get("pay-email", None, type=str)
        if session.get("_requisição"):
            req = Requisição(**session.get("_requisição"))
        else:
            req = Requisição()
        scav = Scav(req)
        caminho = scav.exportar_os_dados()
        enviar_email.delay(email, caminho)
        return redirect(url_for("home.home"))

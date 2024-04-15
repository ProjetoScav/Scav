from flask import request, session


from .funcs.email import enviar_email
from .operador import Scav


def rota_download(blueprint):
    @blueprint.route("/download", methods=["POST"])
    def download():
        scav = Scav()
        scav.checar_cookies(session)
        print("Pedido o download da requisição:", scav.requisição)
        caminho = scav.exportar_os_dados()
        enviar_email(request.get_json()["pay-email"], caminho)
        return "", 204

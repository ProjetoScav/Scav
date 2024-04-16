from flask import request, session

from .operador import Scav, gerar_planilha


def rota_download(blueprint):
    @blueprint.route("/download", methods=["POST"])
    def download():
        email = request.get_json()["pay-email"]
        scav = Scav()
        scav.checar_cookies(session)
        print("Pedido o download da requisição:", scav.requisição)
        gerar_planilha.delay(scav.requisição.as_dict(), email)
        return "", 204

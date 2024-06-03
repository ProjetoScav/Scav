from pathlib import Path

from flask import send_file, session

from app.ext.db.db import db

from .planilha import Planilhador


def rota_download(blueprint):
    @blueprint.route("/download", methods=["POST"])
    def download():
        scav = Planilhador(db)
        scav.checar_cookies(session)
        arquivo = scav.pegar_os_dados()
        # Pedido()
        return send_file(Path("../static") / arquivo)

    @blueprint.route("/pagamento", methods=["POST"])
    def payment():
        ...

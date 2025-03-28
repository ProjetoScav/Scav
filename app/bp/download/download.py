from pathlib import Path

from flask import Blueprint, send_file, session

from app.ext.db.db import db
from app.obj.controllers.planilha.planilhador import Planilhador


def download_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Download
    no Blueprint
    """

    @bp.route("/download", methods=["POST"])
    def download():
        scav = Planilhador(session, db)
        arquivo = scav.pegar_os_dados()
        return send_file(Path("../static") / arquivo)

    return bp

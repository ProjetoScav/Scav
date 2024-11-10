from flask import Blueprint, request
from flask.templating import render_template

from app.ext.cache import cache
from app.ext.db.db import db
from app.obj.classes import CNPJ
from app.obj.controllers.cnpj.gerador import CNPJFront


def cnpj_rota(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de
    CNPJ no Blueprint"""

    @bp.route("/cnpj/<int:estabelecimento_id>")
    @cache.memoize(120)
    def cnpj(estabelecimento_id: int):
        where = request.args.get("where", "home")
        front: CNPJFront = CNPJFront(db, estabelecimento_id)
        cnpj: CNPJ = front.criar_cnpj()
        return render_template("layouts/cnpj.j2", cnpj=cnpj, where=where)

    return bp

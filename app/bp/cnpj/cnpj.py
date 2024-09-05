from flask import Blueprint
from flask.templating import render_template

from app.ext.cache import cache
from app.ext.db.db import db
from app.obj.classes_de_dados import CNPJ
from app.obj.controllers.cnpj.gerador import CNPJFront


def cnpj_rota(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de
    CNPJ no Blueprint"""

    @bp.route("/cnpj/<cnpj>")
    @cache.memoize(120)
    def cnpj(cnpj: str):
        front: CNPJFront = CNPJFront(db, cnpj)
        cnpj_obj: CNPJ = front.criar_cnpj()
        return render_template("pages/cnpj.j2", cnpj=cnpj_obj)

    return bp

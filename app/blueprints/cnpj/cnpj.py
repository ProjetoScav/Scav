from flask import Blueprint
from flask.templating import render_template

from app.ext.cache.cache import cache
from app.ext.db.db import db

from .cnpj_front import CNPJFront


def cnpj_rota(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de
    CNPJ no Blueprint"""

    @bp.route("/cnpj/<cnpj>")
    @cache.memoize(120)
    def cnpj(cnpj):
        front = CNPJFront(db, cnpj)
        cnpj = front.montar_pagina_de_cnpj()
        return render_template("cnpj.jinja.html", cnpj=cnpj)

    return bp

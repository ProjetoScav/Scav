from flask.templating import render_template
from .cnpj_front import CNPJFront
from app.ext.cache.cache import cache
from app.ext.db.db import db


def rota_cnpj(blueprint):
    @blueprint.route("/cnpj/<cnpj>")
    @cache.memoize(60)
    def cnpj(cnpj):
        front = CNPJFront(db, cnpj)
        cnpj = front.montar_pagina_de_cnpj()
        return render_template("cnpj.html", cnpj=cnpj)

from flask import Blueprint, redirect, request, session
from flask.templating import render_template

from app.ext.db.db import db
from app.obj.controllers.resultado.gerador import ResultadoGerador


def home_rotas(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas da
    Homepage no Blueprint"""

    @bp.route("/", methods=["GET"])
    def home():
        card_generator = ResultadoGerador(session, db)
        cards = card_generator.gerar_cards()
        return render_template(
            "pages/index.j2",
            cards=cards,
            n_de_dados=card_generator.query.n_de_cnpjs,
            n_paginas=card_generator.gerar_n_de_paginas(),
            pagina=1,
            preço=card_generator.query.preço,
        )

    @bp.route("/", methods=["POST"])
    def busca():
        campos = request.form.to_dict()
        campos.pop("csrf_token")
        session["query"] = campos
        return redirect("componentes.resultado")

    return bp

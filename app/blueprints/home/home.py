from flask import Blueprint, request, session
from flask.templating import render_template

from app.ext.db.db import db

from .frontend.frontend import HomeFront


def home_rotas(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas da
    Homepage no Blueprint"""

    @bp.route("/", methods=["GET"])
    def home():
        front = HomeFront(db)
        front.checar_cookies(session)
        cards = front.gerar_cards()
        return render_template(
            "index.jinja.html",
            cards=cards,
            n_de_dados=front.query.numero_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=1,
            preço=front.query.preço,
        )

    @bp.route("/resultados", methods=["GET", "POST"])
    def resultado():
        if request.method == "POST":
            campos = request.form.to_dict()
            campos.pop("csrf_token")
            session["query"] = campos

        pagina = request.args.get("pagina", 1, int)
        front = HomeFront(db)
        front.checar_cookies(session)
        cards = front.gerar_cards(pagina)
        return render_template(
            "componentes/resultados.jinja.html",
            cards=cards,
            n_de_dados=front.query.numero_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=pagina,
            preço=front.query.preço,
        )

    return bp

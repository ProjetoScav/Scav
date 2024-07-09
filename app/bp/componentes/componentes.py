from flask import Blueprint, render_template, request, session

from app.ext.db.db import db
from app.obj.controllers.resultado.gerador import ResultadoGerador


def componentes_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Componentes
    no Blueprint"""

    @bp.route("/results", methods=["GET", "POST"])
    def resultado():
        pagina = request.args.get("pagina", 1, int)
        front = ResultadoGerador(session, db)
        cards = front.gerar_cards(pagina)
        return render_template(
            "components/result/result.j2",
            cards=cards,
            n_de_dados=front.query.n_de_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=pagina,
            preço=front.query.preço,
        )

    @bp.route("/scav", methods=["GET"])
    def scav():
        pagina = request.args.get("pagina", 1, int)
        front = ResultadoGerador(session, db)
        cards = front.gerar_cards(pagina)
        return render_template(
            "layouts/login/scav-login.j2",
            cards=cards,
            n_de_dados=front.query.n_de_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=pagina,
            preço=front.query.preço,
        )

    @bp.route("/faq", methods=["GET"])
    def faq():
        return render_template("layouts/login/faq.j2")

    @bp.route("/lists", methods=["GET"])
    def lists():
        return render_template("layouts/login/lists-table.j2")

    return bp

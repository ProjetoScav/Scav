from flask import Blueprint, render_template, request, session

from app.ext.db.db import db
from app.obj.controllers.resultado.gerador import ResultadoGerador


def componentes_rotas(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Componentes
    no Blueprint"""

    @bp.route("/results", methods=["GET", "POST"])
    def resultado():
        pagina = request.args.get("pagina", 1, int)
        front = ResultadoGerador(session, db)
        cards = front.gerar_cards(pagina)
        return render_template(
            "layoutes/components/result/result.j2",
            cards=cards,
            n_de_dados=front.query.n_de_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=pagina,
            preço=front.query.preço,
        )

    return bp

from flask import request, session, redirect, url_for
from flask.templating import render_template

from .funcs.frontend import HomeFront
from app.objetos.requisição import Requisição
from .funcs.auxiliares import formatar_dados_requisição, gerar_faixa_de_cards


def rota_home(app):
    @app.route("/", methods=["GET"])
    def home():
        pagina = request.args.get("pagina", 1, type=int)
        front = HomeFront()

        # TODO: Transformar em função
        if session.get("_requisição"):
            front.selecionar_requisição(Requisição(**session.get("_requisição")))
        else:
            front.selecionar_requisição(Requisição())

        # TODO: Reduzir
        cards_iniciais = front.gerar_dados_cards()
        começo_cards, fim_cards = gerar_faixa_de_cards(pagina)
        cards = cards_iniciais[começo_cards:fim_cards]
        return render_template(
            "index.html",
            cards=cards,
            n_de_dados=front.numero_cnpjs,
            n_paginas=front.numero_paginas_tela,
            pagina=pagina,
        )

    @app.route("/", methods=["POST"])
    def search():
        kwargs = request.form.to_dict()
        kwargs = formatar_dados_requisição(kwargs)
        session["_requisição"] = kwargs
        return redirect(url_for("home.home", pagina=1))

    @app.errorhandler(500)
    def error_handler(e):
        session.pop("_requisição")
        return render_template("index.html", n_de_dados=0, n_paginas=0)

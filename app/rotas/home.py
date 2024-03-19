from flask import request, session, redirect, url_for
from flask.templating import render_template

from app.funcionalidades.frontend import HomeFront
from app.funcs.auxiliares import gerar_faixa_de_cards, formatar_dados_requisição
from app.objetos.requisição import Requisição


def rota_home(app):
    @app.route("/", methods=["GET"])
    def home():
        pagina = request.args.get("pagina", 1, type=int)
        front = HomeFront()

        if session.get("_requisição"):
            front.selecionar_requisição(Requisição(**session.get("_requisição")))
        else:
            front.selecionar_requisição(Requisição())
        
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
        return redirect(url_for("home"))
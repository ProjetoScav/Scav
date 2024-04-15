from flask import redirect, request, session, url_for
from flask.templating import render_template

from .funcs.auxiliares import formatar_dados_requisição
from .funcs.frontend import HomeFront


def rota_home(app):
    @app.route("/", methods=["GET"])
    def home():
        front = HomeFront()
        front.checar_cookies(session)
        cards = front.gerar_faixa_de_cards()
        return render_template(
            "index.html",
            cards=cards,
            n_de_dados=front.numero_cnpjs,
            n_paginas=front.numero_paginas_tela,
            pagina=request.args.get("pagina", 1, type=int),
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

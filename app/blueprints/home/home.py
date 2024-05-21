from flask import redirect, request, session, url_for
from flask.templating import render_template

from app.ext.db.db import db

from .frontend.frontend import HomeFront


def rota_home(app):
    @app.route("/", methods=["GET"])
    def home():
        pagina = request.args.get("pagina", 1, type=int)
        front = HomeFront(db)
        front.checar_cookies(session)
        cards = front.gerar_cards(pagina)
        return render_template(
            "index.html",
            cards=cards,
            n_de_dados=front.query.numero_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=pagina,
            preço=front.query.preço,
        )

    @app.route("/", methods=["POST"])
    def search():
        campos = request.form.to_dict()
        campos.pop("csrf_token")
        session["query"] = campos
        return redirect(url_for("home.home", pagina=1))

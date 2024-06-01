from flask import redirect, request, session, url_for
from flask.templating import render_template

from app.ext.db.db import db

from .frontend.frontend import HomeFront


def rota_home(app):
    @app.route("/", methods=["GET"])
    def home():
        print("cheguei na HOME")
        front = HomeFront(db)
        front.checar_cookies(session)
        print("chequei os cookies")
        cards = front.gerar_cards()
        print("Gerei os cards")
        return render_template(
            "index.jinja.html",
            cards=cards,
            n_de_dados=front.query.numero_cnpjs,
            n_paginas=front.gerar_n_de_paginas(),
            pagina=1,
            preço=front.query.preço,
        )

    @app.route("/resultados", methods=["GET", "POST"])
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

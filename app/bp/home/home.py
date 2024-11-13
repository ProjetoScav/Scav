from flask import Blueprint, redirect, request, session, url_for
from flask.templating import render_template

from app.ext.db.db import db
from app.obj.controllers.resultado.gerador import ResultadoGerador


def home_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas da
    Homepage no Blueprint
    """

    @bp.route("/", methods=["GET"])
    def home():
        card_generator = ResultadoGerador(session, db)
        result = card_generator.generate_search_result()
        return render_template(
            "pages/index.j2",
            result=result,
            messages={"login": "", "name": "", "email": "", "password": ""},
        )

    @bp.route("/", methods=["POST"])
    def busca():
        campos = request.form.to_dict()
        campos.pop("csrf_token")
        session["query"] = campos
        return redirect(url_for("components.resultado"))

    return bp

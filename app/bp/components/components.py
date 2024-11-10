from flask import Blueprint, render_template, request, session
from jinja2_fragments.flask import render_block

from app.ext.db.db import db
from app.obj.controllers.resultado.gerador import ResultadoGerador


def components_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Componentes
    no Blueprint"""

    @bp.route("/results", methods=["GET", "POST"])
    def resultado():
        page = request.args.get("pagina", 1, int)
        front = ResultadoGerador(session, db)
        result = front.generate_search_result(page)
        return render_template("components/result/result.j2", result=result)

    @bp.route("/scav", methods=["GET"])
    def scav():
        n_page = request.args.get("pagina", 1, int)
        front = ResultadoGerador(session, db)
        result = front.generate_search_result(n_page)
        where = request.args.get("page", "home", str)
        if where == "home":
            return render_block(
                "pages/index.j2",
                "content",
                result=result,
                messages={"login": "", "name": "", "email": "", "password": ""},
            )
        return render_template(
            "layouts/scav.j2",
            result=result,
            where=where,
        )

    @bp.route("/faq", methods=["GET"])
    def faq():
        return render_template("layouts/login/faq.j2")

    @bp.route("/lists", methods=["GET"])
    def lists():
        return render_template("layouts/login/lists-table.j2")

    return bp

from flask.templating import render_template
from .funcs.cnpj_front import CNPJFront
from app.ext.cache.cache import cache


def rota_cnpj(blueprint):
    @blueprint.route("/cnpj/<cnpj>")
    @cache.memoize(60)
    def cnpj(cnpj):
        front = CNPJFront()
        cnpj = front.gerar_dados_cnpj(cnpj)
        return render_template("cnpj.html", cnpj=cnpj)

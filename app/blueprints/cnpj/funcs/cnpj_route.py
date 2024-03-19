from flask.templating import render_template
from funcs.cnpj_front import CNPJFront

def rota_cnpj(blueprint): 
    @blueprint.route("/cnpj/<cnpj>")
    def cnpj(cnpj):
        front = CNPJFront()
        cnpj = front.gerar_dados_cnpj(cnpj)
        return render_template("cnpj.html", cnpj=cnpj)

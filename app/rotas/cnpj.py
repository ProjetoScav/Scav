from flask.templating import render_template
from app.funcionalidades.frontend import CNPJFront

def rota_cnpj(app): 
    @app.route("/cnpj/<cnpj>")
    def cnpj(cnpj):
        front = CNPJFront()
        cnpj = front.gerar_dados_cnpj(cnpj)
        return render_template("cnpj.html", cnpj=cnpj)

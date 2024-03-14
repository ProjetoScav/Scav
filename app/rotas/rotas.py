from flask.templating import render_template
from flask import request
from app.funcionalidades.operador import Operador, GarçomDoFront

def configure(app):
    @app.route("/")
    def home():
        pagina = request.args.get('pagina', 1, type=int)
        operador = Operador()
        front = GarçomDoFront(operador.requisição)
        n_paginas = front.numero_paginas_tela
        fim_cards = pagina * 10
        começo_cards = fim_cards - 10
        cards = front.gerar_dados_cards()
        cards = cards[começo_cards: fim_cards]
        return render_template("index.html", 
                               cards=cards, 
                               n_de_dados=front.numero_cnpjs,
                               n_paginas=n_paginas,
                               pagina=pagina)


    @app.route("/cnpj/<int:cnpj>")
    def cnpj(cnpj):
        return render_template("cnpj.html")
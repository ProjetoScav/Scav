import math
from app.conectores.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.objetos.classes_de_dados import CampoDeDados
from app.objetos.requisição import Requisição
from app.funcs.api import pegar_numero_paginas_cnpjs, pegar_dados_frontend
from app.funcs.pagina import scrape_dos_dados


class HomeFront:
    def selecionar_requisição(self, requisição: Requisição):
        self.requisição = requisição
        self.numero_paginas_api, self.numero_cnpjs = (
           pegar_numero_paginas_cnpjs(requisição, n_dados=True)
        )
        self.numero_paginas_tela: int = self.numero_de_paginas_tela()

    def numero_de_paginas_tela(self) -> int:
        if self.numero_cnpjs > 100:
            return 10
        elif self.numero_cnpjs < 10:
            return 1
        else:
            return math.ceil(self.numero_cnpjs / 10)

    def gerar_dados_cards(self):
        cnpjs = []
        for i in range(1, math.ceil(self.numero_paginas_tela / 2) + 1):
            json = self.requisição.gerar_json(i)
            resposta = ApiExtendidaLigação().fazer_a_requisição(json)
            json = resposta.json()
            dados = json["data"]["cnpj"]
            for dado in dados:
                dados_cnpj = pegar_dados_frontend(dado)
                cnpj_objeto = CampoDeDados(**dados_cnpj)
                cnpjs.append(cnpj_objeto)
        return cnpjs


class CNPJFront:
    def gerar_dados_cnpj(self, cnpj: str):
        pagina = ApiCnpjLigação().fazer_a_requisição(cnpj)
        cnpj = scrape_dos_dados(pagina.text)
        return cnpj

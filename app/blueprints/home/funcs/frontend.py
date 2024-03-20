import math
from app.conectores.conectores import ApiExtendidaLigação
from app.objetos.classes_de_dados import CampoDeDados
from app.objetos.requisição import Requisição
from .api import pegar_numero_cnpjs, pegar_numero_paginas, pegar_dados_frontend
from app.config import cache


class HomeFront:
    """Classe que serve os dados pro template da rota Home"""

    def selecionar_requisição(self, requisição: Requisição):
        """Função que recebe uma Requisição e gera dados para uso próprio"""
        self.requisição = requisição
        self.numero_cnpjs = pegar_numero_cnpjs(self.requisição)
        self.numero_paginas_api = pegar_numero_paginas(self.numero_cnpjs)
        self.numero_paginas_tela: int = self.numero_de_paginas_tela()

    def numero_de_paginas_tela(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        if self.numero_cnpjs > 100:
            return 10
        elif self.numero_cnpjs < 10:
            return 1
        return math.ceil(self.numero_cnpjs / 10)

    # TODO: Organizar essa função e Otimizar essa função
    def gerar_dados_cards(self):
        """Função que gera os cards pra pagina da home"""
        cache_key = (
            f"{self.numero_cnpjs}-{self.numero_paginas_api}-{self.numero_paginas_tela}"
        )
        if cached_return := cache.get(cache_key):
            return cached_return
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
        cache.set(cache_key, cnpjs, 0)
        return cnpjs
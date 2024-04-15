import itertools
import math

from flask import abort

from app.ext.cache.cache import cache
from app.objetos.classes_de_dados import CampoDeDados
from app.objetos.requisição import Requisição

from .api import pegar_campos_de_dados_pagina, pegar_numero_cnpjs, pegar_numero_paginas
from .auxiliares import gera_chave_cache_cards, gerar_faixa_de_cards


class HomeFront:
    """Classe que serve os dados pro template da rota Home"""

    def checar_cookies(self, session) -> None:
        if session.get("_requisição"):
            self.selecionar_requisição(Requisição(**session.get("_requisição")))
        else:
            self.selecionar_requisição(Requisição())

    def numero_de_paginas_tela(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        if self.numero_cnpjs > 100:
            return 10
        elif self.numero_cnpjs < 10:
            return 1
        return math.ceil(self.numero_cnpjs / 10)

    def selecionar_requisição(self, requisição: Requisição) -> None:
        """Função que recebe uma Requisição e gera dados para uso próprio"""
        try:
            self.requisição = requisição
            self.numero_cnpjs = pegar_numero_cnpjs(self.requisição)
            self.numero_paginas_api = pegar_numero_paginas(self.numero_cnpjs)
            self.numero_paginas_tela = self.numero_de_paginas_tela()
        except Exception:
            abort(500, "A pesquisa possui erros nos campos!")

    def gerar_cards(self) -> list[CampoDeDados]:
        """Função que gera os cards pra pagina da home"""
        cnpjs = []
        for i in range(1, math.ceil(self.numero_paginas_tela / 2) + 1):
            json = self.requisição.gerar_json(i)
            cnpjs_pagina = pegar_campos_de_dados_pagina(json)
            cnpjs.append(cnpjs_pagina)
        return itertools.chain.from_iterable(cnpjs)

    def gerar_dados_cards(self) -> list[CampoDeDados]:
        """Função que gera os cards pra pagina da home com cache"""
        cache_key = gera_chave_cache_cards(self.requisição)
        if cache.get(cache_key):
            return cache.get(cache_key)
        cnpjs = self.gerar_cards()
        cache.set(cache_key, cnpjs, 0)
        return cnpjs

    def gerar_faixa_de_cards(self, pagina: int = 1) -> list[CampoDeDados]:
        "Função que gera os cards conforme a página a ser exibida"
        cards_iniciais = self.gerar_dados_cards()
        começo_cards, fim_cards = gerar_faixa_de_cards(pagina)
        return cards_iniciais[começo_cards:fim_cards]

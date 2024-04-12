import math
from app.objetos.requisição import Requisição
from .auxiliares import gera_chave_cache_cards
from .api import pegar_numero_cnpjs, pegar_numero_paginas, pegar_campos_de_dados_pagina
from app.extensions import cache
from flask import abort


class HomeFront:
    """Classe que serve os dados pro template da rota Home"""

    # TODO: Reduzir função
    def selecionar_requisição(self, requisição: Requisição):
        """Função que recebe uma Requisição e gera dados para uso próprio"""
        try:
            self.requisição = requisição
            self.numero_cnpjs = pegar_numero_cnpjs(self.requisição)
            self.numero_paginas_api = pegar_numero_paginas(self.numero_cnpjs)
            self.numero_paginas_tela = self.numero_de_paginas_tela()
        except Exception:
            abort(500)
        

    def numero_de_paginas_tela(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        if self.numero_cnpjs > 100:
            return 10
        elif self.numero_cnpjs < 10:
            return 1
        return math.ceil(self.numero_cnpjs / 10)

    def gerar_dados_cards(self):
        """Função que gera os cards pra pagina da home"""
        cache_key = gera_chave_cache_cards(self.requisição)
        if cache.get(cache_key):
            return cache.get(cache_key)
        cnpjs = []
        for i in range(1, math.ceil(self.numero_paginas_tela / 2) + 1):
            json = self.requisição.gerar_json(i)
            cnpjs_pagina = pegar_campos_de_dados_pagina(json)
            cnpjs = cnpjs + cnpjs_pagina
        cache.set(cache_key, cnpjs, 0)
        return cnpjs

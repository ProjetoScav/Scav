import math
from app.ext.db.query.query import Query
from .auxiliares import (
    gerar_cards_cnpj,
    gerar_faixa_de_cards,
)


class HomeFront:
    """Classe que serve os dados pro template da rota Home"""

    def __init__(self, db):
        self.db = db

    def gerar_n_de_paginas(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        if self.query.numero_cnpjs > 100:
            return 10
        elif self.query.numero_cnpjs < 10:
            return 1
        return math.ceil(self.query.numero_cnpjs / 10)

    # TODO: Documentar função
    def checar_cookies(self, session) -> None:
        if campos := session.get("query"):
            self.query = Query(campos, self.db, "card")
        else:
            self.query = Query({"situacao_cadastral": 2}, self.db, "card")
        self.query.gerar_query_filtrada()

    # TODO: Documentar função
    # * Testar yield per - otimização do loading
    # TODO: Cachear essa função
    def gerar_cards(self, pagina: int = 1):
        n_cards = pagina * 10
        começo_cards, fim_cards = gerar_faixa_de_cards(pagina)
        resultados = self.db.session.execute(self.query.query).fetchmany(n_cards)[
            começo_cards:fim_cards
        ]
        return gerar_cards_cnpj(resultados)

import math

from flask_sqlalchemy import SQLAlchemy

from app.ext.db.query.query import Query
from app.obj.classes_de_dados import Card
from app.obj.data.mappers import situacao_cadastral


class ResultadoGerador:
    def __init__(self, session, db: SQLAlchemy):
        self.db = db
        self.query = self.checar_cookies(session)

    def gerar_n_de_paginas(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        if self.query.n_de_cnpjs > 100:
            return 10
        elif self.query.n_de_cnpjs < 10:
            return 1
        return math.ceil(self.query.n_de_cnpjs / 10)

    def __gerar_faixa_de_cards(self, pagina: int) -> tuple[int, int]:
        """Função que recebe o número da pagina da home que deve ser exibida e retorna 
        2 valores que dão o começo e o fim do intervalo dos cards"""
        return (pagina * 10) - 10, pagina * 10

    def __gerar_cards_cnpj(self, resultados) -> list[Card]:
        print(resultados, resultados[0].empresa)
        return [
            Card(
                estabelecimento_id=resultado.estabelecimento_id,
                cnpj=resultado.cnpj_completo,
                municipio=resultado.municipio.municipio,
                estado=resultado.uf,
                cadastro=situacao_cadastral[resultado.situacao_cadastral],
                razao_social=resultado.empresa.razao_social,
            )
            for resultado in resultados
        ]

    # TODO: Documentar função
    def checar_cookies(self, session) -> Query:
        filtros = session.get("query", {"situacao_cadastral": 2})
        return Query(filtros, self.db)

    # TODO: Documentar função
    # * Testar yield per - otimização do loading
    # TODO: Cachear essa função
    def gerar_cards(self, pagina: int = 1) -> list[Card]:
        start_cards, end_cards = self.__gerar_faixa_de_cards(pagina)
        results = self.query.query.slice(start_cards, end_cards).all()
        return self.__gerar_cards_cnpj(results)

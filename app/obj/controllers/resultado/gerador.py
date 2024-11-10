import math
from typing import Any

from flask_sqlalchemy import SQLAlchemy

from app.ext.db.query.query import Query
from app.obj.classes import Card, SearchResult
from app.obj.data.mappers import situacao_cadastral


class ResultadoGerador:
    def __init__(self, session: dict[str, Any], db: SQLAlchemy):
        self.db = db
        self.query = self.check_cookie(session)

    @staticmethod
    def __gerar_faixa_de_cards(pagina: int) -> tuple[int, int]:
        """Função que recebe o número da pagina da home que deve ser exibida e retorna
        2 valores que dão o começo e o fim do intervalo dos cards"""
        return (pagina * 10) - 10, pagina * 10

    @staticmethod
    def __gerar_cards_cnpj(resultados) -> list[Card]:
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

    def generate_n_pages(self) -> int:
        """Função que gera o número de páginas de dados da home"""
        max_pages = 100
        min_page = 10
        if self.query.n_cnpjs > max_pages:
            return 10
        elif self.query.n_cnpjs < min_page:
            return 1
        return math.ceil(self.query.n_cnpjs / 10)

    # TODO: Documentar função
    def check_cookie(self, session: dict[str, Any]) -> Query:
        filtros = session.get("query", {"situacao_cadastral": 2})
        return Query(filtros, self.db)

    # TODO: Documentar função
    # * Testar yield per - otimização do loading
    # TODO: Cachear essa função
    def generate_cards(self, pagina: int = 1) -> list[Card]:
        start_cards, end_cards = self.__gerar_faixa_de_cards(pagina)
        results = self.query.query.slice(start_cards, end_cards).all()
        return self.__gerar_cards_cnpj(results)

    def generate_search_result(self, n_page: int = 1) -> SearchResult:
        return SearchResult(
            n_cnpjs=self.query.n_cnpjs,
            price=self.query.price,
            page=n_page,
            n_pages=self.generate_n_pages(),
            cards=self.generate_cards(n_page),
        )

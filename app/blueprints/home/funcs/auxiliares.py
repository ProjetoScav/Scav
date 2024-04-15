import re

from app.objetos.requisição import Requisição
from app.objetos.variaveis import campos_booleanos, campos_lista


def checar_numero_em_string(string: str) -> bool:
    """Função que recebe uma string e retorna se ela possue números dentro dela"""
    return any(char.isdigit() for char in string)


def extrair_palavras(string: str) -> list[str]:
    """Função que recebe uma string e retorna uma lista das palavras/frases dentro dela"""
    return re.compile(r"\b([A-zÀ-ú\s]+)\b").findall(string)


def extrair_numeros(string: str) -> list[str]:
    """Função que recebe uma string e retorna uma lista com os números dentro dela"""
    return re.compile(r"\d+").findall(string)


def formatar_campo_lista(valor: str) -> list:
    """Função que formata um valor recebido para a requisição e o retorna"""
    if valor:
        if checar_numero_em_string(valor):
            return extrair_numeros(valor)
        return extrair_palavras(valor)
    return []


def formatar_dados_requisição(kwargs: dict) -> dict:
    """Função que formata os dados do cookie para colocar na requisição"""
    kwargs.pop("csrf_token")
    for key, valor in kwargs.items():
        if key in campos_booleanos:
            kwargs[key] = True
        elif key in campos_lista:
            kwargs[key] = formatar_campo_lista(valor.lower())
    return kwargs


def gerar_faixa_de_cards(pagina: int) -> tuple[int, int]:
    """Função que recebe o número da pagina da home que deve ser exibida e retorna 2 valores
    que dão o começo e o fim do intervalo dos cards"""
    return (pagina * 10) - 10, pagina * 10


def gera_chave_cache_cards(requisição: Requisição) -> str:
    """Função que gera uma key da requisição pro cache"""
    return f"{str(requisição.query)} + {str(requisição.extras)} + {str(requisição.range_query)}"

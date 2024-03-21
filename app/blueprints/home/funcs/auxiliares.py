from app.objetos.variaveis import campos_booleanos, campos_lista
from app.objetos.requisição import Requisição


def formatar_campo_lista(value: str) -> list:
    """Função que formata um valor recebido para a requisição e o retorna"""
    if value:
        if "," in value:
            value = value.split(",")
            return value
        value = [value]
        return value
    value = []
    return value


# TODO: Completar e dividir essa função
def formatar_dados_requisição(kwargs: dict) -> dict:
    """Função que formata os dados do cookie para colocar na requisição"""
    kwargs.pop("csrf_token")
    for key, value in kwargs.items():
        if key in campos_booleanos:
            kwargs[key] = True
        elif key in campos_lista:
            value = formatar_campo_lista(value)
            kwargs[key] = value
    return kwargs


def gerar_faixa_de_cards(pagina: int):
    """Função que recebe o número da pagina da home que deve ser exibida e retorna 2 valores
    que dão o começo e o fim do intervalo dos cards"""
    return (pagina * 10) - 10, pagina * 10


def gera_chave_cache_cards(requisição: Requisição) -> str:
    """Função que gera uma key da requisição pro cache"""
    cache_key = f"{str(requisição.query)} + {str(requisição.extras)} + {str(requisição.range_query)}"
    return cache_key

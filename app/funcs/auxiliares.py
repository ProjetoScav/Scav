from typing import Any
from app.objetos.variaveis import campos_booleanos, campos_lista


def formatar_cnpj(cnpj: str):
    return (
        cnpj[:2]
        + "."
        + cnpj[2:5]
        + "."
        + cnpj[5:8]
        + "/"
        + cnpj[8:12]
        + "-"
        + cnpj[12:]
    )


def gerar_string_de_lista(valores: list[str]) -> str:
    """Função que recebe uma lista de strings e
    as junta em uma string só para a planilha"""
    return "".join(valor + ",  " for valor in valores)


def checar_e_remover(valor: Any, lista: list) -> None:
    if valor in lista:
        lista.remove(valor)


def gerar_faixa_de_cards(pagina: int):
    fim_cards = pagina * 10
    começo_cards = fim_cards - 10
    return começo_cards, fim_cards


def formatar_campo_lista(key: str, value: str) -> list:
    if value:
        if "," in value:
            value = value.split(",")
        else:
            value = [key]
    else:
        value = []
    return value


def formatar_dados_requisição(kwargs: dict) -> dict:
    kwargs.pop("csrf_token")
    for key, value in kwargs.items():
        if key in campos_booleanos:
            kwargs[key] = True
        elif key in campos_lista:
            value = formatar_campo_lista(key, value)
            kwargs[key] = value
    return kwargs

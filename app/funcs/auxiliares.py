from typing import Any
from app.objetos.variaveis import campos_booleanos, campos_lista


def gerar_string_de_lista(valores: list[str]) -> str:
    """Função que recebe uma lista de strings e
    as junta em uma string só para a planilha"""
    return "".join(valor + ",  " for valor in valores)

# TODO: Documentar essa função
def checar_e_remover(valor: Any, lista: list) -> None:
    if valor in lista:
        lista.remove(valor)

# TODO: Documentar essa função
def gerar_faixa_de_cards(pagina: int):
    fim_cards = pagina * 10
    começo_cards = fim_cards - 10
    return começo_cards, fim_cards

# TODO: Documentar essa função
def formatar_campo_lista(value: str) -> list:
    if value:
        if "," in value:
            value = value.split(",")
            return value
        value = [value]
        return value
    value = []
    return value


# TODO: Função que remove os valores invalidos no formulário
def remover_valor_invalido(value: str) -> str: ...

# TODO: Documentar essa função
def formatar_dados_requisição(kwargs: dict) -> dict:
    kwargs.pop("csrf_token")
    for key, value in kwargs.items():
        if key in campos_booleanos:
            kwargs[key] = True
        elif key in campos_lista:
            value = formatar_campo_lista(value)
            kwargs[key] = value
    return kwargs

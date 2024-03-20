from typing import Any


def gerar_string_de_lista(valores: list[str]) -> str:
    """Função que recebe uma lista de strings e
    as junta em uma string só para a planilha"""
    return "".join(valor + ",  " for valor in valores)


def checar_e_remover(valor: Any, lista: list) -> None:
    """Função que recebe um valor e uma lista e remove o valor se presente"""
    if valor in lista:
        lista.remove(valor)


# TODO: Função que remove os valores invalidos no formulário
def remover_valor_invalido(value: str) -> str: ...

from typing import Any


def formatar_cnpj(cnpj: str):
    return cnpj[:2] + "." + cnpj[2:5] + "." + cnpj[5:8] + "/" + cnpj[8:12] + "-" + cnpj[12:]


def formatar_numero(numero: str):
    return ("{:,}".format(int(numero))).replace(",", ".")


def formatar_razao_social(razao: str):
    if len(razao) > 59:
        return razao[:59] + razao[59].strip(" ") + "..."
    return razao


def definir_numero_de_pesquisa(n_dados: str):
    n_dados = int(n_dados)
    if n_dados > 1000:
        return 1000
    return n_dados


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

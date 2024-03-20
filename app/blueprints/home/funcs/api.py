from app.conectores.conectores import ApiExtendidaLigação
from app.objetos.requisição import Requisição
import math


def pegar_dados_frontend(dado: dict) -> tuple[str, str, str, str, str]:
    """Função que recebe um arquivo JSON e pega os dados que serão usados nos cards da homepage"""
    cnpj = dado["cnpj"]
    razao = dado["razao_social"]
    cadastro = dado["situacao_cadastral"]
    municipio = dado["municipio"]
    estado = dado["uf"]
    return {
        "razao_social": razao,
        "municipio": municipio,
        "estado": estado,
        "cadastro": cadastro,
        "cnpj": cnpj,
    }


def pegar_numero_cnpjs(requisição: Requisição) -> int:
    """Função que recebe uma requisição e retorna o número de dados na requisição"""
    resposta = ApiExtendidaLigação().fazer_a_requisição(requisição.gerar_json())
    n_dados = int(resposta.json()["data"]["count"])
    return n_dados


def pegar_numero_paginas(n_dados: int) -> int:
    """Função que pega o número de dados e retorna a quantidade de páginas da requisição"""
    if n_dados > 1000:
        return 50
    elif n_dados < 1000 and n_dados > 20:
        return math.ceil(n_dados / 20)
    return 1

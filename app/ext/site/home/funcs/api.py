import math

from flask import abort

from app.ext.api.conectores import ApiExtendidaLigação
from app.objetos.classes_de_dados import CampoDeDados
from app.objetos.requisição import Requisição


def pegar_dados_frontend(dado: dict) -> tuple[str, str, str, str, str]:
    """Função que recebe um arquivo JSON e pega os dados que serão usados nos cards da homepage"""
    return {
        "razao_social": dado["razao_social"],
        "municipio": dado["municipio"],
        "estado": dado["uf"],
        "cadastro": dado["situacao_cadastral"],
        "cnpj": dado["cnpj"],
    }


def pegar_numero_cnpjs(requisição: Requisição) -> int:
    """Função que recebe uma requisição e retorna o número de dados na requisição"""
    resposta = ApiExtendidaLigação().fazer_a_requisição(requisição.gerar_json())
    return int(resposta.json()["data"]["count"])


def pegar_numero_paginas(n_dados: int) -> int:
    """Função que pega o número de dados e retorna a quantidade de páginas da requisição"""
    if n_dados > 1000:
        return 50
    elif n_dados < 1000 and n_dados > 20:
        return math.ceil(n_dados / 20)
    return 1


def gerar_campo_de_dados(dado: dict) -> CampoDeDados:
    """Função que recebe um dicionário com dados de CNPJ e
    retorna um objeto Campo de Dados populado"""
    dados_cnpj = pegar_dados_frontend(dado)
    return CampoDeDados(**dados_cnpj)


def pegar_blocos_cnpj(json: dict) -> list[dict]:
    """Função que faz uma requisição a API da Casa dos Dados e
    retorna uma lista com dicionários que contem os dados dos CNPJs"""
    try:
        resposta = ApiExtendidaLigação().fazer_a_requisição(json)
        json = resposta.json()
        return json["data"]["cnpj"]
    except Exception:
        abort(500)


def pegar_campos_de_dados_pagina(json: dict) -> list[CampoDeDados]:
    """Função que recebe um dicionário com dados de CNPJ e retorna uma lista de Campos de Dados"""
    return [gerar_campo_de_dados(dado) for dado in pegar_blocos_cnpj(json)]

from app.conectores.conectores import ApiExtendidaLigação
from app.objetos.requisição import Requisição
import math


def pegar_os_cnpjs(json: dict) -> list[str]:
    """Função que recebe o JSON da Casa de Dados
    e retorna uma lista de CNPJ's"""
    lista_de_cnpjs = json["data"]["cnpj"]
    cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
    return cnpjs


def pegar_dados_frontend(dado: dict) -> tuple[str, str, str, str, str]:
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
    resposta = ApiExtendidaLigação().fazer_a_requisição(requisição.gerar_json())
    n_dados = int(resposta.json()["data"]["count"])
    return n_dados


def pegar_numero_paginas(n_dados: int) -> int:
    if n_dados < 1000 and n_dados > 20:
        n_paginas = math.ceil(n_dados / 20)
    elif n_dados > 1000:
        n_paginas = 50
    else:
        n_paginas = 1
    return n_paginas

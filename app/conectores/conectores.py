from requests import post, get, Response
from time import sleep


class ApiExtendidaLigação:
    """Classe que faz a requisição a API extendida da Casa de Dados"""

    URL = "https://api.casadosdados.com.br/v2/public/cnpj/search"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    def fazer_a_requisição(self, json: dict) -> Response:
        """Função que faz o request a API da Casa de Dados,
        recebe o JSON com as instruções pra API e retorna um
        objeto Response"""
        try:
            resposta = post(self.URL, json=json, headers=self.headers)
        except Exception as e:
            print(e)
        else:
            if not resposta.status_code == 200:
                print(f"Problema no request: {resposta.status_code}")
                print(resposta.text)
            return resposta


class ApiCnpjLigação:
    """Classe que faz a requisição a API de CNPJS da Casa de Dados"""

    URL = "https://casadosdados.com.br/solucao/cnpj/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    def fazer_a_requisição(self, cnpj: str) -> Response | None:
        """Função que faz o request a API da Casa de Dados,
        recebe o JSON com as instruções pra API e retorna um
        objeto Response"""
        try:
            resposta = get(self.URL + cnpj, headers=self.headers)
        except Exception as e:
            print(e)
        else:
            if not resposta.status_code == 200:
                print(f"Problema no request: {resposta.status_code}")
                print(resposta.text)
            sleep(0.1)
            return resposta

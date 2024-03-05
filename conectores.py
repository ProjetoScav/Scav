import requests
from requests import Response


class ApiExtendidaLigação:
    '''Classe que faz a requisição a API extendida da Casa de Dados'''
    URL = "https://api.casadosdados.com.br/v2/public/cnpj/search"

    headers = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/8.6.1"
    }
    
    def fazer_a_requisição(self, json: dict) -> Response:
        '''Função que faz o request a API da Casa de Dados,
        recebe o JSON com as instruções pra API e retorna um
        objeto Response'''
        try:
            resposta = requests.post(self.URL, json=json, headers=self.headers)
        except Exception as e:
            print(e)
        else:
            if resposta.status_code == 200:
                return resposta 
            else:
                print(f"Problema no request: {resposta.status_code}")
                print(resposta.text)
                return resposta


class ApiCnpjLigação:
    '''Classe que faz a requisição a API de CNPJS da Casa de Dados'''
    URL = "https://casadosdados.com.br/solucao/cnpj/"

    headers = {
    "User-Agent": "insomnia/8.6.1"
    }
    
    def fazer_a_requisição(self, cnpj: str) -> Response | None:
        '''Função que faz o request a API da Casa de Dados,
        recebe o JSON com as instruções pra API e retorna um
        objeto Response'''
        try:
            resposta = requests.get(self.URL + cnpj, headers=self.headers)
        except Exception as e:
            print(e)
        else:
            if resposta.status_code == 200:
                return resposta 
            else:
                print(f"Problema no request: {resposta.status_code}")
                print(resposta.text)
                return resposta
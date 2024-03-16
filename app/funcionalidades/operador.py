from app.funcs.planillha import criar_dataframe, exportar_dataframe
from app.funcs.pagina import scrape_dos_dados

from app.conectores.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.objetos.requisição import Requisição


class Scav:
    """Classe central da aplicação, responsável pelo manejo
    das API's internas e gerar os resultados do programa"""

    def __init__(self):
        self.conector_extendida: ApiExtendidaLigação = ApiExtendidaLigação()
        self.conector_cnpj: ApiCnpjLigação = ApiCnpjLigação()
        self.requisição: Requisição = Requisição()
        self.cnpjs: list = []
        self.paginas: list = []

    def fazer_requisições_cnpj(self):
        """Função que faz a requisição na API da Casa de Dados
        e salvas os cnpjs"""
        numero_paginas = self.pegar_numero_paginas_cnpjs(self.requisição)
        for i in range(1, numero_paginas + 1):
            json = self.requisição.gerar_json(i)
            resposta = self.conector_extendida.fazer_a_requisição(json)
            self.cnpjs = self.cnpjs + self.processador.pegar_os_cnpjs(resposta.json())
            print("cnpjs adicionados")

    def fazer_requisições_dados(self):
        """Função que pega as páginas dos cnpjs na Casa de Dados
        e as salva no objeto"""
        for cnpj in self.cnpjs:
            resposta = self.conector_cnpj.fazer_a_requisição(cnpj)
            self.paginas.append(resposta.text)
            print("Página adicionada")

    def puxar_dados(self):
        """Função que pega os cnpjs e as páginas de cnpjs e
        as salva no objeto"""
        self.fazer_requisições_cnpj()
        self.fazer_requisições_dados()

    def exportar_os_dados(self):
        self.puxar_dados()
        """Função que exporta os dados em um arquivo .xlxs"""
        cnpjs = scrape_dos_dados(self.paginas)
        df = criar_dataframe(cnpjs)
        exportar_dataframe(df)

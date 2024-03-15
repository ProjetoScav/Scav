import math

from app.conectores.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.modelos.objetos import (
    GeradorDeObjetos,
    Requisição,
)

from .processadores import ProcessadorDeDados


class Operador:
    """Classe central da aplicação, responsável pelo manejo
    das API's internas e gerar os resultados do programa"""

    def __init__(self):
        self.conector_extendida: ApiExtendidaLigação = ApiExtendidaLigação()
        self.conector_cnpj: ApiCnpjLigação = ApiCnpjLigação()
        self.processador: ProcessadorDeDados = ProcessadorDeDados()
        self.gerador: GeradorDeObjetos = GeradorDeObjetos()
        self.requisição: Requisição = self.gerador.gerar_requisição()
        self.cnpjs: list = []
        self.paginas: list = []

    # ! Função que tem 2 funções
    def pegar_numero_paginas_cnpjs(
        self, requisição: Requisição, n_dados: bool = False
    ) -> int | tuple[int, int]:
        """Função que recebe uma requisição da Casa dos Dados
        e calcula sua quantidade de páginas"""
        resposta = self.conector_extendida.fazer_a_requisição(requisição.gerar_json())
        n_dados = int(resposta.json()["data"]["count"])

        if n_dados < 1000 and n_dados > 20:
            n_paginas = math.ceil(n_dados / 20)
        elif n_dados > 1000:
            n_paginas = 50
        else:
            n_paginas = 1

        if n_dados:
            return n_paginas, n_dados
        else:
            return n_paginas

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
        cnpjs = self.processador.scrape_dos_dados(self.paginas)
        df = self.processador.criar_dataframe(cnpjs)
        self.processador.exportar_dataframe(df)


class HomeFront:
    def __init__(self, requisição: Requisição):
        self.requisição = requisição
        self.numero_paginas_api, self.numero_cnpjs = (
            Operador().pegar_numero_paginas_cnpjs(requisição, n_dados=True)
        )
        self.numero_paginas_tela: int = self.numero_de_paginas_tela()

    def numero_de_paginas_tela(self) -> int:
        if self.numero_cnpjs > 100:
            return 10
        elif self.numero_cnpjs < 10:
            return 1
        else:
            return math.ceil(self.numero_cnpjs / 10)

    def gerar_dados_cards(self):
        cnpjs = []
        for i in range(1, math.ceil(self.numero_paginas_tela / 2) + 1):
            json = self.requisição.gerar_json(i)
            resposta = ApiExtendidaLigação().fazer_a_requisição(json)
            json = resposta.json()
            dados = json["data"]["cnpj"]
            for dado in dados:
                dados_cnpj = ProcessadorDeDados().pegar_dados_frontend(dado)
                cnpj_objeto = GeradorDeObjetos().gerar_campo_de_dados(*dados_cnpj)
                cnpjs.append(cnpj_objeto)
        return cnpjs


class CNPJFront:
    def gerar_dados_cnpj(self, cnpj: str):
        pagina = ApiCnpjLigação().fazer_a_requisição(cnpj)
        cnpj = ProcessadorDeDados().scrape_dos_dados(pagina.text)
        return cnpj

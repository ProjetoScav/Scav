import math

from conectores import ApiCnpjLigação, ApiExtendidaLigação
from objetos import (
    GeradorDeObjetos,
    MudançaExtras,
    MudançaQuery,
    MudançaRangeQuery,
    Requisição,
)
from processadores import ProcessadorDeDados


class Operador:
    def __init__(self):
        self.conector_extendida: ApiExtendidaLigação = ApiExtendidaLigação()
        self.conector_cnpj: ApiCnpjLigação = ApiCnpjLigação()
        self.processador: ProcessadorDeDados = ProcessadorDeDados()
        self.gerador: GeradorDeObjetos = GeradorDeObjetos()
        self.requisição: Requisição = GeradorDeObjetos().gerar_requisição()
        self.numero_paginas: int = 0
        self.cnpjs: list = []
        self.paginas: list = []

    def modificar_requisição(self, modificações: list[MudançaRangeQuery | MudançaExtras | MudançaQuery]):
        for modificação in modificações:
            if isinstance(modificação, MudançaQuery):
                self.requisição.mudar_query(modificação)
            elif isinstance(modificação, MudançaRangeQuery):
                self.requisição.mudar_range_query(modificação)
            elif isinstance(modificação, MudançaExtras):
                self.requisição.mudar_extras(modificação)
            else:
                print("Modificação não é classe")
    
    def pegar_numero_paginas(self):
        resposta = self.conector_extendida.fazer_a_requisição(self.requisição.gerar_json())
        n_dados = int(resposta.json()["data"]["count"])            
        
        if n_dados < 1000 and n_dados > 20: 
            n_paginas = math.ceil(n_dados / 20)
        elif n_dados > 1000: 
            n_paginas = 50
        else: 
            n_paginas = 1
        
        self.numero_paginas = n_paginas

    def fazer_requisições_cnpj(self):
        self.pegar_numero_paginas()
        for i in range(1, self.numero_paginas + 1):
            json = self.requisição.gerar_json(i)
            resposta = self.conector_extendida.fazer_a_requisição(json)
            self.cnpjs = self.cnpjs + self.processador.pegar_os_cnpjs(resposta.json())
            print("cnpjs adicionados")

    def fazer_requisições_dados(self):
        for cnpj in self.cnpjs:
            resposta = self.conector_cnpj.fazer_a_requisição(cnpj)
            self.paginas.append(resposta.text)
            print("Página adicionada")
    
    def puxar_dados(self):
        self.fazer_requisições_cnpj()
        self.fazer_requisições_dados()

    def exportar_os_dados(self):
        linhas = self.processador.scrape_dos_dados(self.paginas)
        df = self.processador.criar_dataframe(linhas)
        self.processador.exportar_dataframe(df)

filtros = [MudançaRangeQuery("data_abertura", até=None, desde
                             ="2024-03-02"), 
           MudançaQuery("atividade_principal", ["7020400", "6399200", "7420001", "7410299", "9511800", "8599603", "7119703", "7410202", "8130300"]),
           MudançaExtras("com_email", True)]

operador = Operador()
operador.modificar_requisição(filtros)
operador.puxar_dados()
operador.exportar_os_dados()
print(operador.paginas)
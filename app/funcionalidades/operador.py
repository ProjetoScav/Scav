import math

from app.conectores.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.modelos.objetos import (
    GeradorDeObjetos,
    MudançaExtras,
    MudançaQuery,
    MudançaRangeQuery,
    Requisição,
)

from .processadores import ProcessadorDeDados

class Operador:
    '''Classe central da aplicação, responsável pelo manejo 
    das API's internas e gerar os resultados do programa'''
    def __init__(self):
        self.conector_extendida: ApiExtendidaLigação = ApiExtendidaLigação()
        self.conector_cnpj: ApiCnpjLigação = ApiCnpjLigação()
        self.processador: ProcessadorDeDados = ProcessadorDeDados()
        self.gerador: GeradorDeObjetos = GeradorDeObjetos()
        self.requisição: Requisição = self.gerador.gerar_requisição()
        self.requisições: list[Requisição] = []
        self.cnpjs: list = []
        self.paginas: list = []
        self.modificações: list[MudançaRangeQuery | MudançaExtras | MudançaQuery] = []

    def modificar_requisição(self):
        '''Função que faz as alterações na requisição 
        através de uma lista de objetos de mudança'''
        for modificação in self.modificações:
            if isinstance(modificação, MudançaQuery):
                self.requisição.mudar_query(modificação)
            elif isinstance(modificação, MudançaRangeQuery):
                self.requisição.mudar_range_query(modificação)
            elif isinstance(modificação, MudançaExtras):
                self.requisição.mudar_extras(modificação)
            else:
                print("Modificação não é classe")

    def fechar_requisição(self):
        '''Função que coloca a requisição vigente na lista de 
        requisições e gera uma requisição nova'''
        self.requisições.append(self.requisição)
        self.requisição = self.gerador.gerar_requisição()
    
    def pegar_numero_paginas_cnpjs(self, requisição: Requisição) -> int:
        '''Função que recebe uma requisição da Casa dos Dados
        e calcula sua quantidade de páginas'''
        resposta = self.conector_extendida.fazer_a_requisição(requisição.gerar_json())
        n_dados = int(resposta.json()["data"]["count"])            
        
        if n_dados < 1000 and n_dados > 20: 
            n_paginas = math.ceil(n_dados / 20)
        elif n_dados > 1000: 
            n_paginas = 50
        else: 
            n_paginas = 1
        
        return n_paginas, n_dados

    def fazer_requisições_cnpj(self):
        '''Função que faz a requisição na API da Casa de Dados
        e salvas os cnpjs'''
        for requisição in self.requisições:
            numero_paginas, n_dados = self.pegar_numero_paginas_cnpjs(requisição)
            for i in range(1, numero_paginas + 1):
                json = requisição.gerar_json(i)
                resposta = self.conector_extendida.fazer_a_requisição(json)
                self.cnpjs = self.cnpjs + self.processador.pegar_os_cnpjs(resposta.json())
                print("cnpjs adicionados")

    def fazer_requisições_dados(self):
        '''Função que pega as páginas dos cnpjs na Casa de Dados 
        e as salva no objeto'''
        for cnpj in self.cnpjs:
            resposta = self.conector_cnpj.fazer_a_requisição(cnpj)
            self.paginas.append(resposta.text)
            print("Página adicionada")
    
    def puxar_dados(self):
        '''Função que pega os cnpjs e as páginas de cnpjs e 
        as salva no objeto'''
        self.fazer_requisições_cnpj()
        self.fazer_requisições_dados()

    def exportar_os_dados(self):
        self.puxar_dados()
        '''Função que exporta os dados em um arquivo .xlxs'''
        linhas = self.processador.scrape_dos_dados(self.paginas)
        df = self.processador.criar_dataframe(linhas)
        self.processador.exportar_dataframe(df)


class GarçomDoFront:
    def __init__(self, requisição: Requisição):
        self.requisição = requisição
        self.numero_paginas_api, self.numero_cnpjs = Operador().pegar_numero_paginas_cnpjs(requisição)
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
        for i in range(1 , math.ceil(self.numero_paginas_tela / 2) + 1):
            json = self.requisição.gerar_json(i)
            resposta = ApiExtendidaLigação().fazer_a_requisição(json)
            json = resposta.json()
            dados = json["data"]["cnpj"]
            for dado in dados:
                cnpj, razao, municipio, estado, cadastro = ProcessadorDeDados().pegar_dados_frontend(dado) 
                cnpj_objeto = GeradorDeObjetos().gerar_campo_de_dados(
                                                                    razao=razao, 
                                                                    cnpj=cnpj, 
                                                                    cadastro=cadastro,
                                                                    municipio=municipio,
                                                                    estado=estado)
                cnpjs.append(cnpj_objeto)
        return cnpjs
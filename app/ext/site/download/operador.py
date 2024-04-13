import itertools
from multiprocessing.dummy import Pool

from app.ext.api.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.ext.site.home.funcs.api import pegar_numero_cnpjs, pegar_numero_paginas
from .funcs.funcs import pegar_os_cnpjs
from app.funcs.pagina import scrape_dos_dados
from app.objetos.requisição import Requisição

from .planillha import criar_dataframe, exportar_dataframe


class Scav:
    """Classe central da aplicação, responsável pelo manejo
    das API's internas e gerar os resultados do programa"""

    def __init__(self, requisição: Requisição):
        self.conector_extendida = ApiExtendidaLigação()
        self.conector_cnpj = ApiCnpjLigação()
        self.requisição = requisição
        self.paginas: list = []

    def fazer_requisições_cnpj(self):
        """Função que faz a requisição na API da Casa de Dados
        e salvas os cnpjs"""
        numero_paginas = pegar_numero_paginas(pegar_numero_cnpjs(self.requisição))
        jsons = [self.requisição.gerar_json(i) for i in range(1, numero_paginas + 1)]
        with Pool(5) as workers:
            try:
                respostas = workers.map(
                    self.conector_extendida.fazer_a_requisição, jsons
                )
            except Exception:
                pass
        cnpjs_listas = [pegar_os_cnpjs(resposta.json()) for resposta in respostas]
        return itertools.chain.from_iterable(cnpjs_listas)

    def fazer_requisições_dados(self, cnpjs: list):
        """Função que pega as páginas dos cnpjs na Casa de Dados
        e as salva no objeto"""
        with Pool(5) as workers:
            try:
                respostas = workers.map(self.conector_cnpj.fazer_a_requisição, cnpjs)
            except Exception:
                pass
        return [resposta.text for resposta in respostas]

    def puxar_dados(self):
        """Função que pega os cnpjs e as páginas de cnpjs e
        as salva no objeto"""
        cnpjs = self.fazer_requisições_cnpj()
        return self.fazer_requisições_dados(cnpjs)

    def exportar_os_dados(self):
        paginas = self.puxar_dados()
        """Função que exporta os dados em um arquivo .xlxs"""
        cnpjs = scrape_dos_dados(paginas)
        df = criar_dataframe(cnpjs)
        return exportar_dataframe(df)

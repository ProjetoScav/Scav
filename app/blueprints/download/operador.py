import itertools
from multiprocessing.dummy import Pool

from app.blueprints.home.funcs.api import pegar_numero_cnpjs, pegar_numero_paginas
from app.ext.api.conectores import ApiCnpjLigação, ApiExtendidaLigação
from app.ext.fila import fila
from app.funcs.pagina import scrape_dos_dados
from app.objetos.requisição import Requisição

from .funcs.email import enviar_email
from .planillha import criar_dataframe, exportar_dataframe


class Scav:
    """Classe central da aplicação, responsável pelo manejo
    das API's internas e gerar os resultados do programa"""

    def __init__(self):
        self.conector_extendida = ApiExtendidaLigação()
        self.conector_cnpj = ApiCnpjLigação()
        self.paginas: list = []

    def checar_cookies(self, session) -> None:
        """Função que checa o cookie e seta a requisição a ser usada pela instância"""
        if session.get("_requisição"):
            self.requisição = Requisição(**session.get("_requisição"))
        else:
            self.requisição = Requisição()

    def pegar_os_cnpjs(self, json: dict) -> list[str]:
        """Função que recebe o JSON da Casa de Dados e retorna uma lista de CNPJ's"""
        lista_de_cnpjs = json["data"]["cnpj"]
        cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
        return cnpjs

    def fazer_requisições_cnpj(self):
        """Função que faz a requisição na API da Casa de Dados
        e salvas os cnpjs"""
        numero_paginas = pegar_numero_paginas(pegar_numero_cnpjs(self.requisição))
        jsons = [self.requisição.gerar_json(i) for i in range(1, numero_paginas + 1)]
        with Pool(3) as workers:
            try:
                respostas = workers.map(
                    self.conector_extendida.fazer_a_requisição, jsons
                )
            except Exception as e:
                print("Problema na requisição da API:", e)
            else:
                print("As requisições a API foram concluídas com sucesso")
        cnpjs_listas = [
            self.pegar_os_cnpjs(resposta.json()) for resposta in respostas if resposta
        ]
        return list(itertools.chain.from_iterable(cnpjs_listas))

    def fazer_requisições_dados(self, cnpjs: list):
        """Função que pega as páginas dos cnpjs na Casa de Dados
        e as salva no objeto"""
        with Pool(3) as workers:
            try:
                respostas = workers.map(self.conector_cnpj.fazer_a_requisição, cnpjs)
            except Exception as e:
                print("Problema na requisição dos CNPJs por motivo:", e)
            else:
                print("As requisições das páginas foram concluídas com sucesso")
        return [resposta.text for resposta in respostas if resposta]

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
        caminho = exportar_dataframe(df)
        print("Planilha criada com sucesso")
        return caminho


@fila.task(serializer="pickle")
def gerar_planilha(scav: Scav, email: str):
    caminho = scav.exportar_os_dados()
    enviar_email.delay(email, caminho)
    return f"Planilha gerada com sucesso: {scav.requisição}, {email}"

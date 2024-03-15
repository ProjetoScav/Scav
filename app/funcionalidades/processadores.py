from parsel import Selector, SelectorList
from app.modelos.objetos import CNPJ
import pandas as pd
from typing import Any


class ProcessadorDeDados:
    """Classe com as funções que processam dados"""

    def pegar_os_cnpjs(self, json: dict) -> list[str]:
        """Função que recebe o JSON da Casa de Dados
        e retorna uma lista de CNPJ's"""
        lista_de_cnpjs = json["data"]["cnpj"]
        cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
        return cnpjs

    def gerar_string_de_lista(self, valores: list[str]) -> str:
        """Função que recebe uma lista de strings e
        as junta em uma string só para a planilha"""
        return "".join(valor + ",  " for valor in valores)

    def checar_e_remover(self, valor: Any, lista: list) -> None:
        if valor in lista:
            lista.remove(valor)

    # ! Função muito grande
    def extrair_dado_categoria(self, bloco: SelectorList) -> tuple[str, str]:
        """Função que recebe um bloco HTML do Parsel e extrae o valor e a categoria dos dados"""
        categoria = bloco.css(":first-child::text").get()
        seletor = bloco.css(":first-child ~ :not(first-child)::text")

        if valor := bloco.css(":nth-child(2) a::text").get():
            return valor, categoria
        elif bloco.xpath('./p[text()="Quadro Societário"]'):
            nomes = bloco.xpath("./p//b//text()").getall()
            adendos = seletor.getall()
            valores = [nome + adendo for nome, adendo in zip(nomes, adendos)]
            valor = self.gerar_string_de_lista(valores).split(",   ")
            self.checar_e_remover("", valor)
            valor = [socio.strip(",  ") for socio in valor]
        elif bloco.css(":nth-child(2) + p"):
            valores = seletor.getall()
            valor = self.gerar_string_de_lista(valores).split(",  ")
            self.checar_e_remover("", valor)
        else:
            valor = bloco.css(":nth-child(2)::text").get()

        return valor, categoria

    def preencher_cnpj_obj(self, pagina: str) -> CNPJ:
        html = Selector(pagina)
        blocos = html.css(".is-narrow")
        cnpj = CNPJ()
        for bloco in blocos:
            valor, categoria = self.extrair_dado_categoria(bloco)
            categoria = cnpj.setar_valor(categoria, valor)
        return cnpj

    def scrape_dos_dados(self, paginas: str | list) -> list[CNPJ] | CNPJ:
        """Função que recebe uma lista de páginas de CNPJ e retorna uma lista
        contendo os dados de dos CNPJ's como dicionários"""
        if isinstance(paginas, list):
            cnpjs = []
            for pagina in paginas:
                cnpj = self.preencher_cnpj_obj(pagina)
                cnpjs.append(cnpj)
            return cnpjs
        else:
            return self.preencher_cnpj_obj(paginas)

    def pegar_dados_frontend(self, dado: dict) -> tuple[str, str, str, str, str]:
        cnpj = dado["cnpj"]
        razao = dado["razao_social"]
        cadastro = dado["situacao_cadastral"]
        municipio = dado["municipio"]
        estado = dado["uf"]
        return razao, municipio, estado, cadastro, cnpj

    def criar_dataframe(self, linhas: list[CNPJ]) -> pd.DataFrame:
        """Função que recebe uma lista de dicionários e retorna um dataframe"""
        linhas = [linha.transformar_dict() for linha in linhas]
        return pd.DataFrame(linhas)

    def exportar_dataframe(self, df: pd.DataFrame):
        """Função que recebe um dataframe e gera um arquivo Excel com ele"""
        df.to_excel("planilha.xlsx", index=False, engine="openpyxl")

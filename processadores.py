from parsel import Selector, SelectorList
import pandas as pd

class ProcessadorDeDados:
    '''Classe com as funções que processam dados'''
    def pegar_os_cnpjs(self, json: dict) -> list[str]:
        '''Função que recebe o JSON da Casa de Dados 
        e retorna uma lista de CNPJ's'''
        lista_de_cnpjs = json["data"]["cnpj"]
        cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
        return cnpjs
    
    def gerar_string_de_lista(self, valores: list[str]) -> str:
        '''Função que recebe uma lista de strings e 
        as junta em uma string só para a planilha'''
        return ''.join(valor + ", " for valor in valores)
    
    def extrair_dado_categoria(self, bloco: SelectorList) -> tuple[str, str]:
        '''Função que recebe um bloco HTML do Parsel e extrae o valor e a categoria dos dados'''
        categoria = bloco.css(":first-child::text").get()
        seletor = bloco.css(":first-child ~ :not(first-child)::text")

        if valor := bloco.css(":nth-child(2) a::text").get(): 
            return valor, categoria
        elif bloco.xpath('./p[text()="Quadro Societário"]'):
            nomes = bloco.xpath("./p//b//text()").getall()
            adendos = seletor.getall()
            valores = [nome + adendo for nome, adendo in zip(nomes, adendos)]
            valor = self.gerar_string_de_lista(valores)
        elif bloco.css(":nth-child(2) + p"):
            valores = seletor.getall()
            valor = self.gerar_string_de_lista(valores) 
        else:
            valor = bloco.css(":nth-child(2)::text").get()
        
        return valor, categoria
        
    def scrape_dos_dados(self, lista_de_paginas: list[SelectorList]) -> list[dict]:
        '''Função que recebe uma lista de páginas de CNPJ e retorna uma lista 
        contendo os dados de dos CNPJ's como dicionários'''
        linhas = []
        for pagina in lista_de_paginas:
            html = Selector(pagina)
            blocos = html.css(".is-narrow")
            linha_de_dados = {}
            for bloco in blocos:
                valor, categoria = self.extrair_dado_categoria(bloco)
                linha_de_dados[categoria] = valor
            linhas.append(linha_de_dados)
        return linhas
    
    def criar_dataframe(self, linhas: list[dict]) -> pd.DataFrame:
        '''Função que recebe uma lista de dicionários e retorna um dataframe'''
        return pd.DataFrame(linhas) 

    def exportar_dataframe(self, df: pd.DataFrame):
        '''Função que recebe um dataframe e gera um arquivo Excel com ele'''
        df.to_excel("planilha.xlsx", index=False, engine="openpyxl")
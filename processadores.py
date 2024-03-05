from parsel import Selector
import pandas as pd

class ProcessadorDeDados:
    '''Classe com as funções que processam dados'''
    def pegar_os_cnpjs(self, json: dict) -> list[str]:
        '''Função que recebe o JSON da Casa de Dados 
        e retorna uma lista de CNPJ's'''
        lista_de_cnpjs = json["data"]["cnpj"]
        cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
        return cnpjs
    
    # ? Dividir a função
    def scrape_dos_dados(self, lista_de_paginas: list) -> list[dict]:
        '''Função que recebe uma lista de páginas de CNPJ e retorna uma lista 
        contendo os dados de dos CNPJ's como dicionários'''
        linhas = []
        for pagina in lista_de_paginas:
            html = Selector(pagina)
            blocos = html.css(".is-narrow")
            categorias = []
            valores = []
            for bloco in blocos:
                categoria = bloco.css(":first-child::text").get()
                #! Seletor não pega os textos dentro de links
                valor = bloco.css(":nth-child(2)::text").get()
                categorias.append(categoria)
                valores.append(valor)
            linha_de_dados = {categoria: valor for categoria, valor in zip(categorias, valores)}
            linhas.append(linha_de_dados)
        return linhas
    
    def criar_dataframe(self, linhas: list[dict]) -> pd.DataFrame:
        '''Função que recebe uma lista de dicionários e retorna um dataframe'''
        return pd.DataFrame(linhas) 

    def exportar_dataframe(self, df: pd.DataFrame):
        '''Função que recebe um dataframe e gera um arquivo Excel com ele'''
        df.to_excel("planilha.xlsx", index=False, engine="openpyxl")
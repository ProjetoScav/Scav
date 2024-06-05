import random
import string
from pathlib import Path

import pandas as pd

from app.blueprints.cnpj.funcs.auxiliares import transformar_em_cnpj
from app.ext.db.query.query import Query
from app.objetos.classes_de_dados import CNPJ


class Planilhador:
    def __init__(self, db):
        self.db = db

    def checar_cookies(self, session):
        if campos := session.get("query"):
            self.query = Query(campos, self.db)
        else:
            self.query = Query({"situacao_cadastral": 2}, self.db)
        self.query.filtrar_query()

    def __gerar_nome_planilha(self, tipo_de_arquivo: str) -> str:
        """Função que gera o nome da planilha de dados"""
        k = random.randint(5, 10)
        sorteado = random.choices(string.ascii_letters + string.digits, k=k)
        complemento = "".join(sorteado)
        arquivo = f"planilha{complemento}.{tipo_de_arquivo}"
        return arquivo

    def __criar_dataframe(self, cnpjs: list[CNPJ]) -> pd.DataFrame:
        """Método que gera um dataframe de uma lista de CNPJs"""
        df = pd.DataFrame(cnpjs)
        return df

    def __exportar_dataframe(self, df: pd.DataFrame):
        """Função que recebe um dataframe, gera um arquivo Excel com ele e retorna o seu caminho"""
        if len(df) > 1_000_00:
            arquivo = self.__gerar_nome_planilha("csv")
            caminho = Path("./static") / arquivo
            df.to_csv(caminho, index=False, chunksize=250_000)
            return arquivo

        arquivo = self.__gerar_nome_planilha("xlsx")
        caminho = Path("./static") / arquivo
        df.to_excel(caminho, index=False, engine="xlsxwriter")
        return arquivo

    def pegar_os_dados(self):
        iterador = self.query.query.yield_per(1)
        linhas = [
            transformar_em_cnpj(resultado).ajustar_dados_pra_download()
            for resultado in iterador
        ]
        df = self.__criar_dataframe(linhas)
        arquivo = self.__exportar_dataframe(df)
        return arquivo

import random
import string
from pathlib import Path

import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from app.ext.db.query.query import Query
from app.obj.classes import CNPJ
from app.obj.controllers.cnpj.gerador import transformar_em_cnpj


class Planilhador:
    """Classe encarregada do processo
    de geração de planilhas de dados
    """

    def __init__(self, session, db: SQLAlchemy) -> None:
        self.db = db
        self.query = self.check_cookie(session)

    # TODO: Documentar
    def check_cookie(self, session) -> Query:
        filtros = session.get("query", {"situacao_cadastral": 2})
        return Query(filtros, self.db)

    @staticmethod
    def __gerar_nome_planilha(tipo_de_arquivo: str) -> str:
        """Função que gera o nome da planilha de dados"""
        k = random.randint(5, 10)
        sorteado = random.choices(string.ascii_letters + string.digits, k=k)
        complemento = "".join(sorteado)
        arquivo = f"planilha{complemento}.{tipo_de_arquivo}"
        return arquivo

    @staticmethod
    def __criar_dataframe(cnpjs: list[CNPJ]) -> pd.DataFrame:
        """Método que gera um dataframe de uma lista de CNPJs"""
        df = pd.DataFrame(cnpjs)
        return df

    def __exportar_dataframe(self, df: pd.DataFrame) -> str:
        """Função que recebe um dataframe, gera um
        arquivo Excel ou CSV com ele e retorna o seu caminho
        """
        max_rows = 1_000_000
        if len(df) > max_rows:
            arquivo = self.__gerar_nome_planilha("csv")
            caminho = Path("./static") / arquivo
            df.to_csv(caminho, index=False, chunksize=250_000)
            return arquivo

        arquivo = self.__gerar_nome_planilha("xlsx")
        caminho = Path("./static") / arquivo
        df.to_excel(caminho, index=False, engine="xlsxwriter")
        return arquivo

    def pegar_os_dados(self) -> str:
        """Função que busca os dados na DB e transforma
        eles em planilha
        """
        iterador = self.query.query.yield_per(10)
        linhas = [
            transformar_em_cnpj(resultado).ajustar_dados_pra_download()
            for resultado in iterador
        ]
        df = self.__criar_dataframe(linhas)
        arquivo = self.__exportar_dataframe(df)
        return arquivo

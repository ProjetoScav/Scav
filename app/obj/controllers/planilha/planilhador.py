import random
import string
from pathlib import Path

import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from app.ext.db.query.query import Query
from app.obj.classes_de_dados import CNPJ
from app.obj.controllers.cnpj.gerador import transformar_em_cnpj


class Planilhador:
    """Classe encarregada do processo
    de geração de planilhas de dados"""

    def __init__(self, session, db: SQLAlchemy) -> None:
        self.db = db
        self.query = self.checar_cookies(session)

    # TODO: Documentar
    def checar_cookies(self, session) -> Query:
        filtros = session.get("query", {"situacao_cadastral": 2})
        return Query(filtros, self.db)

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

    def __exportar_dataframe(self, df: pd.DataFrame) -> str:
        """Função que recebe um dataframe, gera um
        arquivo Excel ou CSV com ele e retorna o seu caminho"""
        if len(df) > 1_000_00:
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
        eles em planilha"""
        iterador = self.query.query.yield_per(10)
        linhas = [
            transformar_em_cnpj(resultado).ajustar_dados_pra_download()
            for resultado in iterador
        ]
        df = self.__criar_dataframe(linhas)
        arquivo = self.__exportar_dataframe(df)
        return arquivo

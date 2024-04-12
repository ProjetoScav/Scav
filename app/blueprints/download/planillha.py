import random
import string

import pandas as pd

from app.objetos.classes_de_dados import CNPJ


def criar_dataframe(linhas: list[CNPJ]) -> pd.DataFrame:
    """Função que recebe uma lista de dicionários e retorna um dataframe"""
    linhas = [linha.transformar_dict() for linha in linhas]
    return pd.DataFrame(linhas)


def exportar_dataframe(df: pd.DataFrame):
    """Função que recebe um dataframe e gera um arquivo Excel com ele"""
    caminho = (
        "".join(
            random.choices(
                string.ascii_letters + string.digits, k=random.randint(5, 10)
            )
        )
        + ".xlsx"
    )
    df.to_excel(f"./static/planilhas/{caminho}", index=False, engine="openpyxl")
    return caminho

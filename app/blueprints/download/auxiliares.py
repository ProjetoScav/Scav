import random
import string
from typing import Optional

from app.objetos.classes_de_dados import CNPJ


def gerar_nome_planilha(tipo_de_arquivo: str) -> str:
    """Função que gera o nome da planilha de dados"""
    k = random.randint(5, 10)
    sorteado = random.choices(string.ascii_letters + string.digits, k=k)
    complemento = "".join(sorteado)
    arquivo = f"planilha{complemento}.{tipo_de_arquivo}"
    return arquivo



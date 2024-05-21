from sqlalchemy import func, select
from unidecode import unidecode
import re

from ..models import MEI, Atividade, Empresa, Estabelecimento, Municipio


def montar_joins(query):
    query = (
        query.join(Empresa, Estabelecimento.cnpj_basico == Empresa.cnpj_basico)
        .outerjoin(MEI)
        .outerjoin(Municipio)
        .outerjoin(Atividade)
    )
    return query


def montar_query_contagem():
    query = select(func.count()).select_from(Estabelecimento)
    return montar_joins(query)


def montar_query_cnpj():
    query = select(Estabelecimento)
    return montar_joins(query)


def montar_query_cards():
    query = select(
        Estabelecimento.cnpj_completo,
        Empresa.razao_social,
        Estabelecimento.uf,
        Municipio.municipio,
        Estabelecimento.situacao_cadastral,
    )
    return montar_joins(query)


def checar_numero_em_string(string: str) -> bool:
    """Função que recebe uma string e retorna se ela possue números dentro dela"""
    return any(char.isdigit() for char in string)


def transformar_maiscula_sem_acento(valores):
    return [unidecode(valor).upper() for valor in valores]


def extrair_palavras(string: str) -> list[str]:
    """Função que recebe uma string e retorna uma lista das palavras/frases dentro dela"""
    return re.compile(r"\b([A-zÀ-ú\s]+)\b").findall(string)


def extrair_numeros(string: str) -> list[str]:
    """Função que recebe uma string e retorna uma lista com os números dentro dela"""
    return re.compile(r"\d+").findall(string)


def formatar_campo_lista(valor: str) -> list:
    """Função que formata um valor recebido para a requisição e o retorna"""
    if checar_numero_em_string(valor):
        return extrair_numeros(valor)
    return extrair_palavras(valor)

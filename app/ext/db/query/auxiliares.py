from unidecode import unidecode
import re


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

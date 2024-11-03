import os
from typing import Optional

from flask_sqlalchemy import SQLAlchemy

from app.ext.db.models import Atividade, Empresa, Estabelecimento
from app.obj.classes_de_dados import CNPJ
from app.obj.data.mappers import matriz_filial, mei, situacao_cadastral


def transformar_em_cnpj(estabelecimento: Estabelecimento) -> CNPJ:
    """Função que recebe uma entidade Estabelecimento e
    retorna um objeto CNPJ"""
    return CNPJ(
        cnpj=estabelecimento.cnpj_completo,
        razao_social=estabelecimento.empresa.razao_social,
        nome_fantasia=estabelecimento.nome_fantasia,
        tipo=matriz_filial[estabelecimento.matriz_filial],
        data_abertura=estabelecimento.data_abertura,
        cadastro=situacao_cadastral[estabelecimento.situacao_cadastral],
        data_cadastro=estabelecimento.data_situacao_cadastral,
        capital_social=estabelecimento.empresa.capital_social,
        natureza_juridica=montar_natureza_juridica(estabelecimento.empresa),
        mei=montar_mei(estabelecimento),
        logradouro=montar_endereço(estabelecimento),
        numero=estabelecimento.numero,
        complemento=estabelecimento.complemento,
        cep=estabelecimento.cep,
        bairro=estabelecimento.bairro,
        municipio=estabelecimento.municipio.municipio,
        estado=estabelecimento.uf,
        telefones=montar_telefones(estabelecimento),
        email=estabelecimento.email,
        quadro_societario=montar_socios(estabelecimento),
        atividade_principal=montar_atividade_principal(
            estabelecimento.atividade_principal
        ),
        atividades_secundarias=montar_atividades_secundarias(
            estabelecimento.atividades_secundarias
        ),
        data_consulta=os.getenv("DATA_CONSULTA"),
    )


def montar_telefone(ddd: str, numero: str) -> Optional[str]:
    """Função que recebe DDD e número e retorna um número
    de telefone formatado"""
    try:
        if numero and ddd:
            telefone = f"({ddd}) {numero}"
            return telefone
        return None
    except Exception:
        return None


def montar_natureza_juridica(empresa: Empresa) -> str:
    """Função que recebe o modelo SQLAlchemy Empresa e formata os atributos
    de natureza jurídica em uma string"""
    natureza_id = empresa.natureza_juridica_id
    natureza = empresa.natureza_juridica.natureza
    return f"{natureza_id} - {natureza}"


def montar_atividade_principal(atividade: Atividade) -> str:
    """Função que recebe o modelo SQLAlchemy Atividade e formata os atributos
    de atividade princial em uma string"""
    return f"{atividade.atividade_id} - {atividade.atividade}"


def montar_atividades_secundarias(
    estabelecimento: Estabelecimento,
) -> Optional[list[str]]:
    """Função que recebe a entidade Estabelecimento e formata os atributos
    das atividades secundárias em uma string"""
    try:
        lista_de_atividades = estabelecimento.atividades_secundarias
        atividades = [
            f"{atividade.atividade_id} - {atividade.atividade}"
            for atividade in lista_de_atividades
        ]
        return atividades
    except Exception:
        return None


def montar_endereço(estabelecimento: Estabelecimento) -> Optional[str]:
    """Função que retorna o endereço da entidade Estabelecimento"""
    if estabelecimento.tipo_logradouro and estabelecimento.logradouro:
        return estabelecimento.tipo_logradouro + " " + estabelecimento.logradouro
    if estabelecimento.logradouro:
        return estabelecimento.logradouro
    return None


def montar_mei(estabelecimento: Estabelecimento) -> Optional[str]:
    """Função que retorna o atributo MEI da entidade Estabelecimento"""
    try:
        return mei[estabelecimento.empresa.mei.mei]
    except Exception:
        return None


def montar_socios(estabelecimento: Estabelecimento) -> Optional[list[str]]:
    """Função que retorna uma lista com os sócios do Estabelecimento
    formatados"""
    socios = estabelecimento.empresa.socios
    if socios:
        return [
            f"{socio.socio} - {socio.qualificacao.qualificacao}" for socio in socios
        ]
    return None


def montar_telefones(estabelecimento: Estabelecimento) -> list[str | None]:
    """Função que retorna uma lista com os telefones do Estabelecimento
    formatado"""
    return [
        montar_telefone(estabelecimento.ddd_1, estabelecimento.telefone_1),
        montar_telefone(estabelecimento.ddd_2, estabelecimento.telefone_2),
    ]


class CNPJFront:
    """Classe que faz a busca dos dados
    e os organiza pra consumo do template"""

    def __init__(self, db: SQLAlchemy, cnpj: str) -> None:
        self.db = db
        self.query = db.session.query(Estabelecimento).where(
            Estabelecimento.cnpj_completo == cnpj
        )

    def criar_cnpj(self) -> CNPJ:
        """Função que pega os dados do CNPJ na DB
        e retorna um objeto CNPJ"""
        cnpj = self.query.first()
        return transformar_em_cnpj(cnpj)

import os

from app.objetos.classes_de_dados import CNPJ
from app.objetos.mappers import matriz_filial, situacao_cadastral

from .formatadores import (
    montar_atividade_principal,
    montar_atividades_secundarias,
    montar_endereço,
    montar_mei,
    montar_natureza_juridica,
    montar_socios,
    montar_telefones,
)


def transformar_em_cnpj(estabelecimento) -> CNPJ:
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

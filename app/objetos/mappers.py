from app.ext.db.models import MEI, Empresa, Estabelecimento, Municipio

situacao_cadastral = {1: "Nula", 2: "Ativa", 3: "Suspensa", 4: "Inapta", 8: "Baixada"}

matriz_filial = {1: "Matriz", 2: "Filial"}

mei = {"S": "Sim", "N": "Não", "EM BRANCO": "Outros"}


campo_atributo = {
    "termo": (
        Empresa.razao_social,
        Estabelecimento.nome_fantasia,
        Estabelecimento.cnpj_completo,
    ),
    "atividade_principal": Estabelecimento.atividade_principal_id,
    "natureza_juridica": Empresa.natureza_juridica_id,
    "situacao_cadastral": Estabelecimento.situacao_cadastral,
    "uf": Estabelecimento.uf,
    "municipio": Municipio.municipio,
    "bairro": Estabelecimento.bairro,
    "cep": Estabelecimento.cep,
    "ddd": (Estabelecimento.ddd_1, Estabelecimento.ddd_2),
    "data_abertura_desde": Estabelecimento.data_abertura,
    "data_abertura_ate": Estabelecimento.data_abertura,
    "capital_social_desde": Empresa.capital_social,
    "capital_social_ate": Empresa.capital_social,
    "somente_mei": MEI.mei,
    "somente_matriz": Estabelecimento.matriz_filial,
    "com_contato_telefonico": Estabelecimento.telefone_1,
    "incluir_atividade_secundaria": Estabelecimento.atividades_secundarias,
    "somente_fixo": (
        Estabelecimento.tipo_de_telefone_1,
        Estabelecimento.tipo_de_telefone_2,
    ),
    "com_email": Estabelecimento.email,
    "excluir_mei": MEI.mei,
    "somente_filial": Estabelecimento.matriz_filial,
    "somente_celular": (
        Estabelecimento.tipo_de_telefone_1,
        Estabelecimento.tipo_de_telefone_2,
    ),
}

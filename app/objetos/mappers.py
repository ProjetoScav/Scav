from app.ext.db.models import Estabelecimento

situacao_cadastral = {1: "Nula", 2: "Ativa", 3: "Suspensa", 4: "Inapta", 8: "Baixada"}

matriz_filial = {1: "Matriz", 2: "Filial"}

mei = {"S": "Sim", "N": "Não", "EM BRANCO": "Outros"}


campo_atributo = {
    "somente_fixo": (
        Estabelecimento.tipo_de_telefone_1,
        Estabelecimento.tipo_de_telefone_2,
    ),
    "somente_celular": (
        Estabelecimento.tipo_de_telefone_1,
        Estabelecimento.tipo_de_telefone_2,
    ),
}

from .auxiliares import (
    transformar_maiscula_sem_acento,
    montar_query_cards,
    montar_query_cnpj,
    montar_query_contagem,
    formatar_campo_lista,
)
from .listas import (
    campos_de_range,
    campos_igualdade,
    campos_lista,
    campos_not_is,
    campos_numero,
)
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from app.objetos.mappers import campo_atributo
from decimal import Decimal


class Query:
    def __init__(
        self,
        formulario: dict[str, str],
        db: SQLAlchemy,
        tipo_de_query: str = None,
    ):
        self.form = {k: v for k, v in formulario.items() if v}
        self.db = db
        if tipo_de_query == "card":
            self.query = montar_query_cards()
        else:
            self.query = montar_query_cnpj()
        self.count_query = montar_query_contagem()

    def gerar_n_de_cnpjs(self):
        "Função que cria o atributo n_cnpjs dentro da Query"
        self.numero_cnpjs = int(self.db.session.execute(self.count_query).first()[0])

    def gerar_preço(self):
        "Função que cria o atributo preço dentro da Query"
        self.preço = round(Decimal(self.numero_cnpjs) * Decimal("0.001"), 2)

    def limpar_dados(self):
        "Função que faz a limpeza dos dados do form"
        for chave, valor in self.form.items():
            if chave in campos_lista:
                self.form[chave] = formatar_campo_lista(valor)
                if chave in ["municipio", "uf"]:
                    self.form[chave] = transformar_maiscula_sem_acento(self.form[chave])
                elif chave in ["ddd", "natureza_juridica", "atividade_principal"]:
                    self.form[chave] = [int(valor) for valor in self.form[chave]]
            if chave in campos_numero:
                self.form[chave] = int(valor)

    def filtrar_termo(self):
        "Função que cria o filtro do termo na query"
        atributos = campo_atributo["termo"]
        lista_condicionais = []
        for valor in self.form["termo"]:
            for atributo in atributos:
                condicional = atributo.contains(valor)
                lista_condicionais.append(condicional)
        self.query = self.query.where(or_(*lista_condicionais))
        self.count_query = self.count_query.where(or_(*lista_condicionais))

    def filtrar_atividades(self):
        "Função que cria os filtros dos atributos de ativades na query"
        tem_atividade_primaria = "atividade_principal" in self.form.keys()
        tem_atividades_secundarias = "incluir_atividade_secundaria" in self.form.keys()

        if tem_atividade_primaria and tem_atividades_secundarias:
            atividade_principal = campo_atributo["atividade_principal"]
            atividades_secundarias = campo_atributo["incluir_atividade_secundaria"]

            condicionais = []
            for valor in self.form["atividade_principal"]:
                condicional_sec = atividades_secundarias.contains(valor)
                condicional_prin = atividade_principal == int(valor)
                condicionais.extend([condicional_prin, condicional_sec])
            self.query = self.query.where(or_(*condicionais))
            self.count_query = self.count_query.where(or_(*condicionais))

        elif tem_atividade_primaria:
            atividade_principal = campo_atributo["atividade_principal"]
            self.query = self.query.where(
                atividade_principal.in_(self.form["atividade_principal"])
            )
            self.count_query = self.count_query.where(
                atividade_principal.in_(self.form["atividade_principal"])
            )

    def filtrar_com_lista(self, chave: str):
        """Função que cria os filtros com comparações em lista
        da query"""
        atributo = campo_atributo[chave]
        valor = self.form[chave]
        if chave == "ddd":
            self.query = self.query.where(
                atributo[0].in_(valor), atributo[1].in_(valor)
            )
            self.count_query = self.count_query.where(
                atributo[0].in_(valor), atributo[1].in_(valor)
            )
        else:
            self.query = self.query.where(atributo.in_(valor))
            self.count_query = self.count_query.where(atributo.in_(valor))

    def filtrar_com_igualdade(self, chave: str):
        "Função que cria os filtros com igualdades na query"
        atributo = campo_atributo[chave]
        valor = self.form[chave]
        if chave in ["somente_fixo", "somente_celular"]:
            self.query = self.query.where(
                or_(atributo[0] == valor, atributo[1] == valor)
            )
            self.count_query = self.count_query.where(
                or_(atributo[0] == valor, atributo[1] == valor)
            )
            print(self.query)
        else:
            self.query = self.query.where(atributo == valor)
            self.count_query = self.count_query.where(atributo == valor)

    def filtrar_ranges(self, chave: str):
        "Função que cria os filtros de range na query"
        atributo = campo_atributo[chave]
        valor = self.form[chave]
        if chave in ["data_abertura_desde", "capital_social_desde"]:
            self.query = self.query.where(atributo >= valor)
            self.count_query = self.count_query.where(atributo >= valor)
        else:
            self.query = self.query.where(atributo <= valor)
            self.count_query = self.count_query.where(atributo <= valor)

    def filtrar_com_is_not(self, chave: str):
        """Faz a filtragem com a exclusão de valores"""
        atributo = campo_atributo[chave]
        valor = self.form[chave]
        if chave == "excluir_mei":
            self.query = self.query.where(atributo.is_not(valor))
            self.count_query = self.count_query.where(atributo.is_not(valor))
        else:
            self.query = self.query.where(atributo.is_not(None))
            self.count_query = self.count_query.where(atributo.is_not(None))

    def gerar_query_filtrada(self):
        "Função que faz todo o processo de montagem da query"
        self.limpar_dados()
        for chave in self.form.keys():
            print(chave)
            self.filtrar_atividades()
            if chave == "termo":
                self.filtrar_termo()
            elif chave in campos_lista and chave != "atividade_principal":
                self.filtrar_com_lista(chave)
            elif chave in campos_igualdade:
                self.filtrar_com_igualdade(chave)
            elif chave in campos_de_range:
                self.filtrar_ranges(chave)
            elif chave in campos_not_is:
                self.filtrar_com_is_not(chave)
        self.gerar_n_de_cnpjs()
        self.gerar_preço()

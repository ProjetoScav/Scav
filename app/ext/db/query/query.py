from .auxiliares import (
    transformar_maiscula_sem_acento,
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
from app.ext.db.models import Estabelecimento
from app.ext.db.filtros import lista_de_filtros


class Query:
    def __init__(
        self,
        formulario: dict[str, str],
        db: SQLAlchemy,
    ):
        self.form = {k: v for k, v in formulario.items() if v}
        self.db = db
        self.query = db.session.query(Estabelecimento)

    def gerar_n_de_cnpjs(self):
        "Função que cria o atributo n_cnpjs dentro da Query"
        self.numero_cnpjs = self.query.count()

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
                elif chave in ["natureza_juridica", "atividade_principal"]:
                    self.form[chave] = [int(valor) for valor in self.form[chave]]
            if chave in campos_numero:
                self.form[chave] = int(valor)

    def filtrar_query(self):
        self.limpar_dados()
        for filtro in lista_de_filtros:
            self.query = filtro(self.form).filtrar(self.query)
        self.gerar_n_de_cnpjs()
        self.gerar_preço()

from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy

from app.ext.db.filtros import lista_de_filtros
from app.ext.db.models import Estabelecimento

from .auxiliares import formatar_campo_lista, transformar_maiscula_sem_acento
from .listas import campos_lista, campos_numero


class Query:
    def __init__(
        self,
        formulario: dict[str, str | int],
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
            print(chave, valor)
            if chave in campos_lista:
                self.form[chave] = formatar_campo_lista(valor)
                print(self.form[chave], type(self.form[chave]))
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
        print("n_cnpjs")
        self.gerar_preço()
        print("preço")

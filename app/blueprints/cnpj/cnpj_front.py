from app.ext.db.models import Estabelecimento
from app.ext.db.query.query import montar_query_cnpj
from app.objetos.classes_de_dados import CNPJ

from .funcs.auxiliares import transformar_em_cnpj


class CNPJFront:
    """Classe que faz a busca dos dados e os
    organiza pra consumo do template
    """

    def __init__(self, db, cnpj: str):
        self.db = db
        self.query = montar_query_cnpj().where(Estabelecimento.cnpj_completo == cnpj)

    def montar_pagina_de_cnpj(self) -> CNPJ:
        """Função que busca os dados e os prepara pro uso no frontend

        Returns:
            CNPJ: Uma classe populada com os dados utilizados no template
        """
        cnpj = self.db.session.scalar(self.query)
        return transformar_em_cnpj(cnpj, self.db)

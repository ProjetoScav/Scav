from flask_sqlalchemy import SQLAlchemy

from app.ext.db.models import Estabelecimento
from app.objetos.classes_de_dados import CNPJ

from .funcs.auxiliares import transformar_em_cnpj


class CNPJFront:
    """Classe que faz a busca dos dados e os
    organiza pra consumo do template
    """

    def __init__(self, db: SQLAlchemy, cnpj: str) -> None:
        self.db = db
        self.query = db.session.query(Estabelecimento).where(
            Estabelecimento.cnpj_completo == cnpj
        )

    def montar_pagina_de_cnpj(self) -> CNPJ:
        """Função que busca os dados e os prepara pro uso no frontend

        Returns:
            CNPJ: Uma classe populada com os dados utilizados no template
        """
        cnpj = self.query.first()
        return transformar_em_cnpj(cnpj)

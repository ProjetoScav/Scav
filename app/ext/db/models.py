import datetime as dt
from typing import List

from flask_login import UserMixin
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from .db import db

engine = create_engine("sqlite:///instance/database.db", echo=True)
session = Session(engine)


class Empresa(db.Model):
    __tablename__ = "empresas"
    cnpj: Mapped[int] = mapped_column(primary_key=True)
    razao_social: Mapped[str] = mapped_column(nullable=False)
    natureza_juridica_id: Mapped[int] = mapped_column(
        ForeignKey("naturezas.natureza_id"), nullable=False
    )
    capital_social: Mapped[float] = mapped_column(nullable=False)
    socios: Mapped[List["Socio"]] = relationship()
    estabelecimentos: Mapped[List["Estabelecimento"]] = relationship(
        back_populates="empresa"
    )
    natureza_juridica: Mapped["Natureza"] = relationship()
    mei: Mapped["MEI"] = relationship()

    def __repr__(self) -> str:
        return f"Empresa(cnpj={self.cnpj}, razao_social={self.razao_social})"


class Estabelecimento(db.Model):
    __tablename__ = "estabelecimentos"
    estabelecimento_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    cnpj_completo: Mapped[int] = mapped_column(nullable=False, unique=True)
    cnpj: Mapped[int] = mapped_column(ForeignKey("empresas.cnpj"), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(nullable=True)
    matriz_filial: Mapped[int] = mapped_column(nullable=True)
    situacao_cadastral: Mapped[int] = mapped_column(nullable=True)
    data_situacao_cadastral: Mapped[dt.date] = mapped_column(nullable=True)
    data_abertura: Mapped[dt.date] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    telefone_1: Mapped[int] = mapped_column(nullable=True)
    telefone_2: Mapped[int] = mapped_column(nullable=True)
    tipo_de_telefone_1: Mapped[str] = mapped_column(nullable=True)
    tipo_de_telefone_2: Mapped[str] = mapped_column(nullable=True)
    ddd_1: Mapped[int] = mapped_column(nullable=True)
    ddd_2: Mapped[int] = mapped_column(nullable=True)
    municipio_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.municipio_id"), nullable=True
    )
    uf: Mapped[str] = mapped_column(String(2), nullable=True)
    bairro: Mapped[str] = mapped_column(nullable=True)
    cep: Mapped[int] = mapped_column(nullable=True)
    tipo_logradouro: Mapped[str] = mapped_column(nullable=True)
    logradouro: Mapped[str] = mapped_column(nullable=True)
    numero: Mapped[str] = mapped_column(nullable=True)
    complemento: Mapped[str] = mapped_column(nullable=True)
    atividade_principal_id: Mapped[int] = mapped_column(
        ForeignKey("atividades.atividade_id"), nullable=True
    )
    atividades_secundarias: Mapped[str] = mapped_column(nullable=True)
    atividade_principal: Mapped["Atividade"] = relationship()
    empresa: Mapped["Empresa"] = relationship(back_populates="estabelecimentos")
    municipio: Mapped["Municipio"] = relationship()

    def __repr__(self) -> str:
        return f"Estabelecimentos(cnpj={self.cnpj_completo})"


class Socio(db.Model):
    __tablename__ = "socios"
    socio_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cnpj: Mapped[int] = mapped_column(ForeignKey("empresas.cnpj"))
    socio: Mapped[str] = mapped_column(nullable=False)
    qualificacao_socio: Mapped[int] = mapped_column(
        ForeignKey("qualificacoes.qualificacao_id")
    )
    qualificacao: Mapped["Qualificacao"] = relationship()

    def __repr__(self) -> str:
        return f"Socio(socio={self.socio}, cnpj={self.cnpj})"


class MEI(db.Model):
    __tablename__ = "meis"
    cnpj: Mapped[int] = mapped_column(ForeignKey("empresas.cnpj"), primary_key=True)
    mei: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"MEI(cnpj={self.cnpj}, mei={self.mei})"


class Municipio(db.Model):
    __tablename__ = "municipios"
    municipio_id: Mapped[int] = mapped_column(primary_key=True)
    municipio: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Municipio(municipio={self.municipio}, id={self.municipio_id})"


class Atividade(db.Model):
    __tablename__ = "atividades"
    atividade_id: Mapped[int] = mapped_column(primary_key=True)
    atividade: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Atividade(atividade={self.atividade}, id={self.atividade_id})"


class Qualificacao(db.Model):
    __tablename__ = "qualificacoes"
    qualificacao_id: Mapped[int] = mapped_column(primary_key=True)
    qualificacao: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"Qualificação(qualificação={self.qualificacao}, id={self.qualificacao_id})"
        )


class Natureza(db.Model):
    __tablename__ = "naturezas"
    natureza_id: Mapped[int] = mapped_column(primary_key=True)
    natureza: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Natureza(qualificação={self.natureza}, id={self.natureza_id})"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(156), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, email={self.email}, listas={self.listas})"

    def get_id(self):
        return self.user_id


# db.Model.metadata.drop_all(engine)
# db.Model.metadata.create_all(engine)

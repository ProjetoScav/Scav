import datetime as dt
from typing import List

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import db


class Empresa(db.Model):
    __tablename__ = "empresas"
    cnpj_basico: Mapped[str] = mapped_column(String(8), primary_key=True)
    natureza_juridica_id: Mapped[int] = mapped_column(
        ForeignKey("naturezas.natureza_id"), nullable=False
    )
    razao_social: Mapped[str] = mapped_column(nullable=False)
    capital_social: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    socios: Mapped[List["Socio"]] = relationship()
    estabelecimentos: Mapped[List["Estabelecimento"]] = relationship(
        back_populates="empresa"
    )
    natureza_juridica: Mapped["Natureza"] = relationship()
    mei: Mapped["MEI"] = relationship()

    def __repr__(self) -> str:
        return f"Empresa(cnpj={self.cnpj_basico}, razao_social={self.razao_social})"


class Estabelecimento(db.Model):
    __tablename__ = "estabelecimentos"
    cnpj_completo: Mapped[str] = mapped_column(String(14), primary_key=True)
    cnpj_basico: Mapped[str] = mapped_column(
        String(8), ForeignKey("empresas.cnpj_basico"), nullable=False
    )
    nome_fantasia: Mapped[str] = mapped_column(nullable=True)
    matriz_filial: Mapped[int] = mapped_column(nullable=False)
    situacao_cadastral: Mapped[int] = mapped_column(nullable=False)
    data_situacao_cadastral: Mapped[dt.date] = mapped_column(nullable=True)
    data_abertura: Mapped[dt.date] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    telefone_1: Mapped[int] = mapped_column(nullable=True)
    telefone_2: Mapped[int] = mapped_column(nullable=True)
    tipo_de_telefone_1: Mapped[str] = mapped_column(String(5), nullable=True)
    tipo_de_telefone_2: Mapped[str] = mapped_column(String(5), nullable=True)
    ddd_1: Mapped[int] = mapped_column(nullable=True)
    ddd_2: Mapped[int] = mapped_column(nullable=True)
    cidade_id: Mapped[int] = mapped_column(
        ForeignKey("municipios.municipio_id"), nullable=True
    )
    uf: Mapped[str] = mapped_column(String(2), nullable=True)
    bairro: Mapped[str] = mapped_column(nullable=True)
    cep: Mapped[int] = mapped_column(nullable=True)
    tipo_logradouro: Mapped[str] = mapped_column(nullable=True)
    logradouro: Mapped[str] = mapped_column(nullable=True)
    numero: Mapped[int] = mapped_column(nullable=True)
    complemento: Mapped[str] = mapped_column(nullable=True)
    atividade_principal_id: Mapped[int] = mapped_column(
        ForeignKey("atividades.atividade_id"), nullable=False
    )
    atividades_secundarias_ids: Mapped[str] = mapped_column(nullable=True)
    atividades_secundarias: Mapped[List["Atividade"]] = relationship(
        secondary="atividades_secundarias", back_populates="estabelecimentos"
    )
    atividade_principal: Mapped["Atividade"] = relationship()
    empresa: Mapped["Empresa"] = relationship(back_populates="estabelecimentos")
    municipio: Mapped["Municipio"] = relationship()

    def __repr__(self) -> str:
        return f"Estabelecimentos(cnpj={self.cnpj_completo})"


class Socio(db.Model):
    __tablename__ = "socios"
    cnpj_basico: Mapped[str] = mapped_column(
        String(8), ForeignKey("empresas.cnpj_basico"), primary_key=True
    )
    socio: Mapped[str] = mapped_column(primary_key=True)
    qualificacao_socio: Mapped[int] = mapped_column(
        ForeignKey("qualificacoes.qualificacao_id"), nullable=False
    )
    qualificacao: Mapped["Qualificacao"] = relationship()

    def __repr__(self) -> str:
        return f"Socio(socio={self.socio}, cnpj={self.cnpj_basico})"


class MEI(db.Model):
    __tablename__ = "meis"
    cnpj_basico: Mapped[str] = mapped_column(
        ForeignKey("empresas.cnpj_basico"), primary_key=True
    )
    mei: Mapped[str] = mapped_column(primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f"MEI(cnpj={self.cnpj_basico}, mei={self.mei})"


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
    estabelecimentos: Mapped[List["Estabelecimento"]] = relationship(
        secondary="atividades_secundarias", back_populates="atividades_secundarias"
    )

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


class AtividadeSecundaria(db.Model):
    __tablename__ = "atividades_secundarias"
    atividade_id: Mapped[int] = mapped_column(
        ForeignKey("atividades.atividade_id"), primary_key=True
    )
    cnpj_completo: Mapped[str] = mapped_column(
        String(8), ForeignKey("estabelecimentos.cnpj_completo"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"AtividadeSecundaria(atividade_id={self.atividade_id}, cnpj_da_atividade={self.cnpj_completo})"


class Pedido(db.Model):
    __tablename__ = "pedidos"
    pedido_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False)
    termo: Mapped[str] = mapped_column(nullable=True)
    atividade_principal: Mapped[str] = mapped_column(nullable=True)
    natureza_juridica: Mapped[str] = mapped_column(nullable=True)
    situacao_cadastral: Mapped[int] = mapped_column(nullable=True)
    uf: Mapped[str] = mapped_column(nullable=True)
    municipio: Mapped[str] = mapped_column(nullable=True)
    bairro: Mapped[str] = mapped_column(nullable=True)
    cep: Mapped[str] = mapped_column(nullable=True)
    ddd: Mapped[str] = mapped_column(nullable=True)
    data_abertura_desde: Mapped[dt.date] = mapped_column(nullable=True)
    data_abertura_ate: Mapped[dt.date] = mapped_column(nullable=True)
    somente_mei: Mapped[str] = mapped_column(nullable=True)
    somente_matriz: Mapped[str] = mapped_column(nullable=True)
    com_contato_telefonico: Mapped[str] = mapped_column(nullable=True)
    incluir_atividade_secundaria: Mapped[str] = mapped_column(nullable=True)
    somente_fixo: Mapped[str] = mapped_column(nullable=True)
    com_email: Mapped[str] = mapped_column(nullable=True)
    excluir_mei: Mapped[str] = mapped_column(nullable=True)
    somente_filial: Mapped[str] = mapped_column(nullable=True)
    somente_celular: Mapped[str] = mapped_column(nullable=True)
    valor: Mapped[int] = mapped_column(nullable=False)
    horario: Mapped[dt.datetime] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Pedido(pedido_id={self.pedido_id}, email={self.email})"

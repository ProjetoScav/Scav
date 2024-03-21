from dataclasses import dataclass, asdict
from .variaveis import campos_mapper


@dataclass
class CNPJ:
    cnpj: str | None = None
    razao_social: str | None = None
    nome_fantasia: str | None = None
    tipo: str | None = None
    data_abertura: str | None = None
    cadastro: str | None = None
    data_cadastro: str | None = None
    capital_social: str | None = None
    natureza_juridica: str | None = None
    mei: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    cep: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    estado: str | None = None
    telefone: str | None = None
    email: str | None = None
    quadro_societario: list | None = None
    atividade_principal: str | None = None
    atividade_secundaria: str | list | None = None
    data_consulta: str | None = None

    def setar_valor(self, categoria: str, valor: str):
        categoria_mapeada = campos_mapper[categoria]
        setattr(self, categoria_mapeada, valor)

    def transformar_dict(self) -> dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class CampoDeDados:
    cnpj: str
    municipio: str
    estado: str
    cadastro: str
    razao_social: str

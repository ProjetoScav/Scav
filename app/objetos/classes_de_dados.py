from dataclasses import asdict, dataclass
from typing import Optional


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
    telefones: str | None = None
    email: str | None = None
    quadro_societario: list | None = None
    atividade_principal: str | None = None
    atividades_secundarias: str | list | None = None
    data_consulta: str | None = None

    def transformar_dict(self) -> dict[str, str]:
        "Método que transforma a classe em um dicionário"
        return {k: str(v) for k, v in asdict(self).items()}

    def _lista_to_string(self, lista: list) -> Optional[str]:
        """Método que converte uma lista em uma string pra planilha"""
        try:
            lista = [f"{item}," for item in lista if item]
            return "".join(lista)[:-1]
        except Exception:
            return None

    def ajustar_dados_pra_download(self):
        "Método que ajusta os dados pra inserção na planilha"
        cnpj = self.transformar_dict()
        for chave in ["telefones", "quadro_societario", "atividades_secundarias"]:
            if cnpj[chave]:
                cnpj[chave] = self._lista_to_string(cnpj[chave])
        return cnpj


@dataclass
class Card:
    cnpj: str
    municipio: str
    estado: str
    cadastro: str
    razao_social: str

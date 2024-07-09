from dataclasses import asdict, dataclass
from typing import Optional

from app.ext.db.models import Estabelecimento


@dataclass
class CNPJ:
    estabelecimento: Estabelecimento

    def extrair_propriedades(self):
        self.__setattr__()
        ...

    def transformar_em_dicionario(self) -> dict[str, str]:
        "Método que transforma a classe em um dicionário"
        return {k: str(v) for k, v in asdict(self).items()}

    def __lista_to_string(self, lista: list) -> Optional[str]:
        """Método que converte uma lista em uma string pra planilha"""
        try:
            lista = [f"{item}," for item in lista if item]
            return "".join(lista)[:-1]
        except Exception:
            return None

    def ajustar_dados_pra_download(self) -> Optional[str]:
        "Método que ajusta os dados pra inserção na planilha"
        cnpj = self.transformar_em_dicionario()
        for chave in ("telefones", "quadro_societario", "atividades_secundarias"):
            if valor := cnpj[chave]:
                cnpj[chave] = self.__lista_to_string(valor)
        return cnpj

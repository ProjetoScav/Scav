from dataclasses import asdict, dataclass, field
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
    telefones: list[str | None] | None = None
    email: str | None = None
    quadro_societario: list | None = None
    atividade_principal: str | None = None
    atividades_secundarias: str | list | None = None
    data_consulta: str | None = None

    @staticmethod
    def __lista_to_string(lista: list) -> Optional[str]:
        """Método que converte uma lista em uma string pra planilha."""
        try:
            lista = [f"{item}," for item in lista if item]
            return "".join(lista)[:-1]
        except Exception:
            return None

    def transformar_em_dicionario(self) -> dict[str, str]:
        """Método que transforma a classe em um dicionário."""
        return {k: str(v) for k, v in asdict(self).items()}

    def ajustar_dados_pra_download(self):
        """Método que ajusta os dados pra inserção na planilha."""
        cnpj = self.transformar_em_dicionario()
        for chave in ["telefones", "quadro_societario", "atividades_secundarias"]:
            if cnpj[chave]:
                cnpj[chave] = self.__lista_to_string(cnpj[chave])
        return cnpj


@dataclass
class Card:
    estabelecimento_id: int
    cnpj: str
    municipio: str
    estado: str
    cadastro: str
    razao_social: str

    def __post_init__(self):
        if self.cadastro == "Ativa":
            self.cadastro_color = "green"
        else:
            self.cadastro_color = "grey"


@dataclass
class SearchResult:
    n_cnpjs: int
    page: int
    n_pages: int
    price: float
    cards: list[Card]

    def __post_init__(self):
        self.has_cnpjs = self.n_cnpjs > 0


@dataclass
class LoginPopupMessages:
    login: str = ""
    register_name: str = ""
    register_email: list[str] = field(default_factory=list)
    register_password: str = ""

    def check_input_error(self, attr: str):
        match attr:
            case "login":
                if self.login:
                    return "input--error"
            case "register_name":
                if self.register_name:
                    return "input--error"
            case "register_email":
                if self.register_email:
                    return "input--error"
            case "register_password":
                if self.register_password:
                    return "input--error"
        return ""

    def validate_register(self) -> bool:
        if self.register_name or self.register_name or self.register_password:
            print(self.register_name, self.register_email, self.register_password)
            return False
        print(self.register_name, self.register_email, self.register_password)
        return True

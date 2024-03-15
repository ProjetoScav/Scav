from dataclasses import dataclass, asdict

campos_mapper = {
    "CNPJ": "cnpj",
    "Nome Fantasia": "nome_fantasia",
    "Razão Social": "razao_social",
    "Tipo": "tipo",
    "Data Abertura": "data_abertura",
    "Situação Cadastral": "cadastro",
    "Data da Situação Cadastral": "data_cadastro",
    "Capital Social": "capital_social",
    "Natureza Jurídica": "natureza_juridica",
    "Empresa MEI": "mei",
    "Logradouro": "logradouro",
    "Número": "numero",
    "Complemento": "complemento",
    "CEP": "cep",
    "Bairro": "bairro",
    "Município": "municipio",
    "UF": "estado",
    "Telefone": "telefone",
    "E-MAIL": "email",
    "Quadro Societário": "quadro_societario",
    "Atividade Principal": "atividade_principal",
    "Atividades Secundárias": "atividade_secundaria",
    "Data da Consulta": "data_consulta",
}


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


class Requisição:
    """Classe que monta o JSON para ser enviado à Casa de Dados"""
    def __init__(
        self,
        termo: list = [],
        atividade_principal: list = [],
        natureza_juridica: list = [],
        uf: list = [],
        municipio: list = [],
        bairro: list = [],
        situacao_cadastral: str = "ATIVA",
        cep: list = [],
        ddd: list = [],
        data_abertura_desde: str | None = None,
        data_abertura_ate: str | None = None,
        capital_social_desde: str | None = None,
        capital_social_ate: str | None = None,
        somente_mei: bool = False,
        excluir_mei: bool = False,
        com_email: bool = False,
        incluir_atividade_secundaria: bool = False,
        com_contato_telefonico: bool = False,
        somente_fixo: bool = False,
        somente_celular: bool = False,
        somente_matriz: bool = False,
        somente_filial: bool = False,
    ):
        self.query = {
            "query": {
                "termo": termo,
                "atividade_principal": atividade_principal,
                "natureza_juridica": natureza_juridica,
                "uf": uf,
                "municipio": municipio,
                "bairro": bairro,
                "situacao_cadastral": situacao_cadastral,
                "cep": cep,
                "ddd": ddd,
            }
        }
        self.range_query = {
            "range_query": {
                "data_abertura": {"lte": data_abertura_ate, "gte": data_abertura_desde},
                "capital_social": {
                    "lte": capital_social_ate,
                    "gte": capital_social_desde,
                },
            }
        }
        self.extras = {
            "extras": {
                "somente_mei": somente_mei,
                "excluir_mei": excluir_mei,
                "com_email": com_email,
                "incluir_atividade_secundaria": incluir_atividade_secundaria,
                "com_contato_telefonico": com_contato_telefonico,
                "somente_fixo": somente_fixo,
                "somente_celular": somente_celular,
                "somente_matriz": somente_matriz,
                "somente_filial": somente_filial,
            }
        }

    def gerar_json(self, pagina: int = 1) -> dict:
        """Função que gera o json à ser enviado,
        recebe o parâmetro página e retorna o JSON"""
        json = {**self.query, **self.range_query, **self.extras, "page": pagina}
        return json


class GeradorDeObjetos:
    def gerar_requisição(self):
        """Função que gera um objeto Requisição"""
        return Requisição()

    def gerar_campo_de_dados(
        self, razao: str, municipio: str, estado: str, cadastro: str, cnpj: str
    ) -> CampoDeDados:
        return CampoDeDados(
            razao_social=razao,
            municipio=municipio,
            estado=estado,
            cadastro=cadastro,
            cnpj=cnpj,
        )

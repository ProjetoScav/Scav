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
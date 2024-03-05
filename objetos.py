from dataclasses import dataclass

# Estruturas de dados que guardam as mudanças no JSON
@dataclass
class MudançaExtras:
    '''Classe de dados que representa uma mudança nas categorias extras do JSON'''
    opção: str
    booleano: bool


@dataclass
class MudançaQuery:
    '''Classe de dados que representa uma mudança nas categorias query do JSON'''
    opção: str
    filtros: list[str] 


@dataclass
class MudançaRangeQuery:
    '''Classe de dados que representa uma mudança nas categorias range query do JSON'''
    opção: str
    desde: str | None
    até: str | None


class Requisição:
    '''Classe que monta o JSON para ser enviado à Casa de Dados'''
    query = {
        "query": {
            "termo": [],
            "atividade_principal": [],
            "natureza_juridica": [],
            "uf": [],
            "municipio": [],
            "bairro": [],
            "situacao_cadastral": "ATIVA",
            "cep": [],
            "ddd": []
        }
    }
    range_query = {
        "range_query": {
            "data_abertura": {
                "lte": None,
                "gte": None
            },
            "capital_social": {
                "lte": None,
                "gte": None
            }
        }
    }
    extras = {
        "extras": {
            "somente_mei": False,
            "excluir_mei": False,
            "com_email": False,
            "incluir_atividade_secundaria": False,
            "com_contato_telefonico": False,
            "somente_fixo": False,
            "somente_celular": True,
            "somente_matriz": False,
            "somente_filial": False
        }
    }

    def mudar_extras(self, mudança: MudançaExtras):
        '''Método que muda as opções da categoria extras do JSON,
        recebe uma lista de objetos MudançaExtras'''
        self.extras["extras"][mudança.opção] = mudança.booleano
    
    def mudar_query(self, mudança: MudançaQuery):
        '''Método que muda as opções da categoria query do JSON,
        recebe uma lista de objetos MudançaQuery'''
        self.query["query"][mudança.opção] = mudança.filtros
            
    def mudar_range_query(self, mudança: MudançaRangeQuery):
        '''Método que muda as opções da categoria range query do JSON,
        recebe uma lista de objetos MudançaRageQuery'''
        if mudança.desde:
            self.range_query["range_query"][mudança.opção]["gte"] = mudança.desde
        if mudança.até:            
            self.range_query["range_query"][mudança.opção]["lte"] = mudança.até

    def gerar_json(self, pagina: int = 1) -> dict:
        '''Função que gera o json à ser enviado, 
        recebe o parâmetro página e retorna o JSON'''
        json = {
            **self.query,
            **self.range_query,
            **self.extras,
            "page": pagina
        }
        return json


class GeradorDeObjetos:
    def gerar_mudança_extras(self, opção: str, booleano: bool) -> MudançaExtras:
        '''Função que gera um objeto MudançaExtra'''
        return MudançaExtras(opção, booleano)

    def gerar_mudança_query(self, opção: str, filtros: list) -> MudançaQuery:
        '''Função que gera um objeto MudançaQuery'''
        return MudançaQuery(opção, filtros)

    def gerar_mudança_range_query(self, opção: str, desde: str | None, até: str | None) -> MudançaRangeQuery:
        '''Função que gera um objeto MudançaRangeQuery'''
        return MudançaRangeQuery(opção, desde, até)

    def gerar_requisição(self):
        '''Função que gera um objeto Requisição'''
        return Requisição()
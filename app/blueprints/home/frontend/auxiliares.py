from app.objetos.classes_de_dados import Card
from app.objetos.mappers import situacao_cadastral


def gerar_faixa_de_cards(pagina: int) -> tuple[int, int]:
    """Função que recebe o número da pagina da home que deve ser exibida e retorna 2 valores
    que dão o começo e o fim do intervalo dos cards"""
    return (pagina * 10) - 10, pagina * 10


def gera_chave_cache_cards(query):
    return str(query)


def gerar_cards_cnpj(resultados) -> list[Card]:
    return [
        Card(
            cnpj=resultado[0],
            municipio=resultado[3],
            estado=resultado[2],
            cadastro=situacao_cadastral[resultado[4]],
            razao_social=resultado[1],
        )
        for resultado in resultados
    ]

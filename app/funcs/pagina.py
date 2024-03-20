from parsel import Selector, SelectorList
from .auxiliares import gerar_string_de_lista, checar_e_remover
from app.objetos.classes_de_dados import CNPJ


# ! Função muito grande
def extrair_dado_categoria(bloco: SelectorList) -> tuple[str, str]:
    """Função que recebe um bloco HTML do Parsel e extrae o valor e a categoria dos dados"""
    categoria = bloco.css(":first-child::text").get()
    seletor = bloco.css(":first-child ~ :not(first-child)::text")

    if valor := bloco.css(":nth-child(2) a::text").get():
        return valor, categoria
    elif bloco.xpath('./p[text()="Quadro Societário"]'):
        nomes = bloco.xpath("./p//b//text()").getall()
        adendos = seletor.getall()
        valores = [nome + adendo for nome, adendo in zip(nomes, adendos)]
        valor = gerar_string_de_lista(valores).split(",   ")
        checar_e_remover("", valor)
        valor = [socio.strip(",  ") for socio in valor]
    elif bloco.css(":nth-child(2) + p"):
        valores = seletor.getall()
        valor = gerar_string_de_lista(valores).split(",  ")
        checar_e_remover("", valor)
    else:
        valor = bloco.css(":nth-child(2)::text").get()

    return valor, categoria


def preencher_cnpj_obj(pagina: str) -> CNPJ:
    """Função que extrae os dados de uma pagina de CNPJ e retorna um objeto CNPJ populado pelos dados"""
    html = Selector(pagina)
    blocos = html.css(".is-narrow")
    cnpj = CNPJ()
    for bloco in blocos:
        valor, categoria = extrair_dado_categoria(bloco)
        categoria = cnpj.setar_valor(categoria, valor)
    return cnpj


def scrape_dos_dados(paginas: str | list) -> list[CNPJ] | CNPJ:
    """Função que recebe uma lista de páginas de CNPJ ou um único,
    e retorna uma lista contendo os dados de um dos CNPJ's como dicionários"""
    if isinstance(paginas, list):
        cnpjs = []
        for pagina in paginas:
            cnpj = preencher_cnpj_obj(pagina)
            cnpjs.append(cnpj)
        return cnpjs
    return preencher_cnpj_obj(paginas)

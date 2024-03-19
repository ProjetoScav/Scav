from app.funcs.pagina import scrape_dos_dados
from app.conectores.conectores import ApiCnpjLigação
# TODO: Documentar essa função
class CNPJFront:
    def gerar_dados_cnpj(self, cnpj: str):
        pagina = ApiCnpjLigação().fazer_a_requisição(cnpj)
        cnpj = scrape_dos_dados(pagina.text)
        return cnpj

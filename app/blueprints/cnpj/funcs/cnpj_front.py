from app.funcs.pagina import scrape_dos_dados
from app.conectores.conectores import ApiCnpjLigação


class CNPJFront:
    """Classe que serve os dados pro frontend da pagina de CNPJ"""

    def gerar_dados_cnpj(self, cnpj: str):
        """Função que gera os dados pra popular uma pagina CNPJ"""
        pagina = ApiCnpjLigação().fazer_a_requisição(cnpj)
        return scrape_dos_dados(pagina.text)

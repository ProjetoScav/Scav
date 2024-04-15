def formatar_cnpj(cnpj: str):
    """Função que recebe uma string de números e a retorna formatada como CNPJ"""
    return (
        cnpj[:2]
        + "."
        + cnpj[2:5]
        + "."
        + cnpj[5:8]
        + "/"
        + cnpj[8:12]
        + "-"
        + cnpj[12:]
    )


def formatar_numero(numero: str):
    """Função que recebe um número em string e o retorna pontuado"""
    return ("{:,}".format(int(numero))).replace(",", ".")


def formatar_razao_social(razao: str):
    """Função que recebe uma string e se ela tiver mais de 59 caracteres ele a encerra com ..."""
    if len(razao) > 59:
        return razao[:59] + razao[59].strip(" ") + "..."
    return razao


def definir_numero_de_pesquisa(n_dados: str):
    """Função que recebe um número em string e retorna o número de dados que podem ser baixados"""
    n_dados = int(n_dados)
    if n_dados > 1000:
        return 1000
    return n_dados

def formatar_cnpj(cnpj: int) -> str:
    """Função que recebe uma string de números e a retorna
    formatada como CNPJ
    """
    cnpj = str(cnpj)
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


def formatar_data(data: str) -> str:
    """Função que recebe uma data em formato YYYY-MM-dd
    e retorna em dd/MM/YYYY
    """
    try:
        ano = data[:4]
        mes = data[5:7]
        dia = data[8:]
        return f"{dia}/{mes}/{ano}"
    except Exception:
        return data


def formatar_numero(numero: str) -> str:
    """Função que recebe um número em string e o retorna pontuado"""
    return ("{:,}".format(int(numero))).replace(",", ".")


def formatar_razao_social(razao: str) -> str:
    """Função que recebe uma string e se ela tiver mais de
    59 caracteres ele a encerra com ...
    """
    try:
        n_digitos = 59
        if len(razao) > n_digitos:
            return razao[:59] + razao[59].strip(" ") + "..."
        return razao
    except Exception:
        return razao


# TODO: Completar os CEPs com 0
def formatar_cep(cep: int) -> str:
    """Função que coloca um . antes dos últimos 3 digitos de um CEP"""
    cep = str(cep)
    n_digitos = 8
    n_cep = len(cep)
    if n_cep < n_digitos:
        return cep
    cep = cep[:8]
    return f"{cep[:5]}.{cep[5:]}"

def formatar_cnpj(cnpj: str) -> str:
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


def formatar_data(data: str) -> str:
    """Função que recebe uma data em formato YYYY-MM-dd
    e retorna em dd/MM/YYYY"""
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
    """Função que recebe uma string e se ela tiver mais de 59 caracteres ele a encerra com ..."""
    try:
        if len(razao) > 59:
            return razao[:59] + razao[59].strip(" ") + "..."
        return razao
    except Exception:
        return razao


def formatar_cep(cep: str) -> str:
    """Função que coloca um . antes dos últimos 3 digitos de um CEP"""
    if len(cep) < 8:
        return cep
    cep = cep[:8]
    return f"{cep[:5]}.{cep[5:]}"

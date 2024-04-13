def pegar_os_cnpjs(json: dict) -> list[str]:
    """Função que recebe o JSON da Casa de Dados e retorna uma lista de CNPJ's"""
    lista_de_cnpjs = json["data"]["cnpj"]
    cnpjs = [cnpj["cnpj"] for cnpj in lista_de_cnpjs]
    return cnpjs
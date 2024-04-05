from flask_caching import Cache

cache = Cache()


def formatar_cnpj(cnpj: str):
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
    return ("{:,}".format(int(numero))).replace(",", ".")


def formatar_razao_social(razao: str):
    if len(razao) > 59:
        return razao[:59] + razao[59].strip(" ") + "..."
    return razao


def definir_numero_de_pesquisa(n_dados: str):
    n_dados = int(n_dados)
    if n_dados > 1000:
        return 1000
    return n_dados

def configurar_extensões(app):
    app.jinja_env.filters["cnpj_format"] = formatar_cnpj
    app.jinja_env.filters["numero_format"] = formatar_numero
    app.jinja_env.filters["razao_format"] = formatar_razao_social
    app.jinja_env.filters["data_number"] = definir_numero_de_pesquisa
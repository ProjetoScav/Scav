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


def configurar_filtros_jinja(app):
    app.jinja_env.filters["cnpj_format"] = formatar_cnpj

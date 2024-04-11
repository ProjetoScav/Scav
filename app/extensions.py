from flask_caching import Cache

from .funcs.auxiliares import (
    definir_numero_de_pesquisa,
    formatar_cnpj,
    formatar_numero,
    formatar_razao_social,
)

cache = Cache()


def configurar_extensões(app):
    app.jinja_env.filters["cnpj_format"] = formatar_cnpj
    app.jinja_env.filters["numero_format"] = formatar_numero
    app.jinja_env.filters["razao_format"] = formatar_razao_social
    app.jinja_env.filters["data_number"] = definir_numero_de_pesquisa

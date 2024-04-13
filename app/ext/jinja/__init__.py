from . import filtros as f


def registrar_filtros(app):
    app.jinja_env.filters["cnpj_format"] = f.formatar_cnpj
    app.jinja_env.filters["numero_format"] = f.formatar_numero
    app.jinja_env.filters["razao_format"] = f.formatar_razao_social
    app.jinja_env.filters["data_number"] = f.definir_numero_de_pesquisa

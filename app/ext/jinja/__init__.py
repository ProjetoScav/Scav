from flask import Flask
from datetime import datetime
from . import filtros as f


def registrar_filtros(app: Flask) -> None:
    """Função que faz o registro dos filtros Jinja no App"""
    app.jinja_env.filters["cnpj_format"] = f.formatar_cnpj
    app.jinja_env.filters["numero_format"] = f.formatar_numero
    app.jinja_env.filters["razao_format"] = f.formatar_razao_social
    app.jinja_env.filters["date_format"] = f.formatar_data
    app.jinja_env.filters["cep_format"] = f.formatar_cep
    app.jinja_env.filters["strftime"] = datetime.strftime

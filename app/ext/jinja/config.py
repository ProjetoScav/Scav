from datetime import datetime

from flask import Flask
from jinja2 import select_autoescape

from . import filtros as f


def jinja_config(app: Flask) -> Flask:
    """Função que faz a configuração do Jinja no App"""
    app.jinja_env.autoescape = select_autoescape(
        ("j2", "html"), default_for_string=True, default=True
    )
    app.jinja_env.filters["cnpj_format"] = f.formatar_cnpj
    app.jinja_env.filters["numero_format"] = f.formatar_numero
    app.jinja_env.filters["razao_format"] = f.formatar_razao_social
    app.jinja_env.filters["date_format"] = f.formatar_data
    app.jinja_env.filters["cep_format"] = f.formatar_cep
    app.jinja_env.filters["strftime"] = datetime.strftime
    return app

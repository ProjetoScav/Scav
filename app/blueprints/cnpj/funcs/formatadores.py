from app.objetos.mappers import mei


# TODO: Type hint
def montar_telefone(ddd: str, numero: str) -> str | None:
    """Função que recebe DDD e número e retorna um número
    de telefone formatado"""
    try:
        if numero and ddd:
            telefone = f"({ddd}) {numero}"
            return telefone
    except Exception:
        return None


# TODO: Type Hint
def montar_natureza_juridica(empresa) -> str:
    """Função que recebe o modelo SQLAlchemy Empresa e formata os atributos
    de natureza jurídica em uma string"""
    natureza_id = empresa.natureza_juridica_id
    natureza = empresa.natureza_juridica.natureza
    return f"{natureza_id} - {natureza}"


# TODO: Type Hint
def montar_atividade_principal(atividade) -> str:
    """Função que recebe o modelo SQLAlchemy Atividade e formata os atributos
    de atividade princial em uma string"""
    return f"{atividade.atividade_id} - {atividade.atividade}"


# TODO: Type Hint
def montar_atividades_secundarias(estabelecimento) -> list[str] | None:
    """Função que recebe o modelo SQLAlchemy Estabelecimento e formata os atributos
    das atividades secundárias em uma string"""
    try:
        lista_de_atividades = estabelecimento.atividades_secundarias
        atividades = [
            f"{atividade.atividade_id} - {atividade.atividade}"
            for atividade in lista_de_atividades
        ]
        return atividades
    except Exception:
        return None


# TODO: Documentar essa função
def montar_endereço(estabelecimento):
    if estabelecimento.tipo_logradouro and estabelecimento.logradouro:
        return estabelecimento.tipo_logradouro + " " + estabelecimento.logradouro
    if estabelecimento.logradouro:
        return estabelecimento.logradouro
    return None


# TODO: Documentar essa função
def montar_mei(estabelecimento):
    try:
        return mei[estabelecimento.empresa.mei.mei]
    except Exception:
        return None


# TODO: Documentar essa função
def montar_socios(estabelecimento):
    socios = estabelecimento.empresa.socios
    if socios:
        return [
            f"{socio.socio} - {socio.qualificacao.qualificacao}" for socio in socios
        ]


# TODO: Documentar essa função
def montar_telefones(estabelecimento):
    return [
        montar_telefone(estabelecimento.ddd_1, estabelecimento.telefone_1),
        montar_telefone(estabelecimento.ddd_2, estabelecimento.telefone_2),
    ]

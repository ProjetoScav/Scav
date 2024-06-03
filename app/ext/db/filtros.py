from abc import abstractmethod, ABC
from app.ext.db.models import Estabelecimento, Empresa, Municipio, MEI
from sqlalchemy import or_


class Filtro(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def filtrar(self, query):
        ...


class FiltroTermo(Filtro):
    def __init__(self, dados_formulario: dict):
        if dados_formulario.get("termo", None):
            self.tem_termo = True
            self.valores = dados_formulario["termo"]
            print(self.valores, type(self.valores))
        else:
            self.tem_termo = False

    def filtrar(self, query):
        if self.tem_termo:
            atributos_simples = (
                Estabelecimento.nome_fantasia,
                Estabelecimento.cnpj_completo,
            )
            lista_condicionais = []
            for valor in self.valores:
                condicional = Estabelecimento.empresa.has(
                    Empresa.razao_social.contains(valor)
                )
                lista_condicionais.append(condicional)
                for atributo in atributos_simples:
                    condicional = atributo.contains(valor)
                    lista_condicionais.append(condicional)
            return query.where(or_(*lista_condicionais))
        return query


class FiltroAtividades(Filtro):
    def __init__(self, dados_formulario):
        incluir_atividades_secundarias = dados_formulario.get(
            "incluir_atividade_secundaria", None
        )
        atividade_primaria = dados_formulario.get("atividade_principal", None)
        if incluir_atividades_secundarias and atividade_primaria:
            self.tem_atividade_secundaria = True
        else:
            self.tem_atividade_secundaria = False
        self.valores = atividade_primaria
        print(self.valores)

    def filtrar(self, query):
        if self.valores:
            atividade_principal = Estabelecimento.atividade_principal_id
            if self.tem_atividade_secundaria:
                atividades_secundarias = Estabelecimento.atividades_secundarias_ids
                condicionais = []
                for valor in self.valores:
                    condicional_sec = atividades_secundarias.contains(valor)
                    condicional_prin = atividade_principal == int(valor)
                    condicionais.extend([condicional_prin, condicional_sec])
                    return query.where(or_(*condicionais))
            return query.where(atividade_principal.in_(self.valores))
        return query


class FiltroNaturezaJuridica(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"natureza_juridica": valores}:
                self.tem_natureza_juridica = True
                self.valores = valores
            case _:
                self.tem_natureza_juridica = False

    def filtrar(self, query):
        if self.tem_natureza_juridica:
            condicional = Estabelecimento.empresa.has(
                Empresa.natureza_juridica_id.in_(self.valores)
            )
            return query.where(condicional)
        return query


class FiltroDDD(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"ddd": valores}:
                self.tem_ddd = True
                self.valores = valores
            case _:
                self.tem_ddd = False

    def filtrar(self, query):
        if self.tem_ddd:
            condicional_1 = Estabelecimento.ddd_1.in_(self.valores)
            condicional_2 = Estabelecimento.ddd_2.in_(self.valores)
            return query.where(or_(condicional_1, condicional_2))
        return query


class FiltroMunicipio(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"municipio": valores}:
                self.tem_municipio = True
                self.valores = valores
            case _:
                self.tem_municipio = False

    def filtrar(self, query):
        if self.tem_municipio:
            condicional = Estabelecimento.municipio.has(
                Municipio.municipio.in_(self.valores)
            )
            return query.where(condicional)
        return query


class FiltroBairro(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"bairro": valores}:
                self.tem_bairro = True
                self.valores = valores
            case _:
                self.tem_bairro = False

    def filtrar(self, query):
        if self.tem_bairro:
            condicional = Estabelecimento.bairro.in_(self.valores)
            return query.where(condicional)
        return query


class FiltroCEP(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"cep": valores}:
                self.tem_cep = True
                self.valores = valores
            case _:
                self.tem_cep = False

    def filtrar(self, query):
        if self.tem_cep:
            condicional = Estabelecimento.cep.in_(self.valores)
            return query.where(condicional)
        return query


class FiltroUF(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"uf": valores}:
                self.tem_uf = True
                self.valores = valores
            case _:
                self.tem_uf = False

    def filtrar(self, query):
        if self.tem_uf:
            condicional = Estabelecimento.uf.in_(self.valores)
            return query.where(condicional)
        return query


class FiltroSituacaoCadastral(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"situacao_cadastral": valor}:
                self.tem_situacao_cadastral = True
                self.valor = valor
            case _:
                self.tem_situacao_cadastral = False

    def filtrar(self, query):
        if self.tem_situacao_cadastral:
            condicional = Estabelecimento.situacao_cadastral == self.valor
            return query.where(condicional)
        return query


class FiltroDataDeAbertura(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"data_abertura_desde": data_desde, "data_abertura_ate": data_ate}:
                self.tem_data_desde_ate = True
                self.data_desde = data_desde
                self.data_ate = data_ate
            case {"data_abertura_ate": data_ate}:
                self.tem_data_desde_ate = False
                self.tem_data_ate = True
                self.tem_data_desde = False
                self.data = data_ate
            case {"data_abertura_desde": data_desde}:
                self.tem_data_desde_ate = False
                self.tem_data_desde = True
                self.tem_data_ate = False
                self.data = data_desde
            case _:
                self.tem_data_desde_ate = False
                self.tem_data_desde = False
                self.tem_data_ate = False

    def filtrar(self, query):
        if self.tem_data_desde_ate:
            condicional = Estabelecimento.data_abertura.between(
                self.data_desde, self.data_ate
            )
            return query.where(condicional)
        elif self.tem_data_desde:
            condicional = Estabelecimento.data_abertura >= self.data
            return query.where(condicional)

        elif self.tem_data_ate:
            condicional = Estabelecimento.data_abertura <= self.data
            return query.where(condicional)
        return query


class FiltroCapitalSocial(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {
                "capital_social_desde": capital_desde,
                "capital_social_ate": capital_ate,
            }:
                self.tem_capital_desde_ate = True
                self.capital_desde = capital_desde
                self.capital_ate = capital_ate
            case {"capital_social_ate": capital_ate}:
                self.tem_capital_desde_ate = False
                self.tem_capital_ate = True
                self.tem_capital_desde = False
                self.capital = capital_ate
            case {"capital_social_desde": capital_desde}:
                self.tem_capital_desde_ate = False
                self.tem_capital_desde = True
                self.tem_capital_ate = False
                self.capital = capital_desde
            case _:
                self.tem_capital_desde_ate = False
                self.tem_capital_desde = False
                self.tem_capital_ate = False

    def filtrar(self, query):
        if self.tem_capital_desde_ate:
            condicional = Estabelecimento.empresa.has(
                Empresa.capital_social.between(self.capital_desde, self.capital_ate)
            )
            return query.where(condicional)
        elif self.tem_capital_desde:
            condicional = Estabelecimento.empresa.has(
                Empresa.capital_social >= self.capital
            )
            return query.where(condicional)

        elif self.tem_capital_ate:
            condicional = Estabelecimento.empresa.has(
                Empresa.capital_social <= self.capital
            )
            return query.where(condicional)
        return query


class FiltroSomenteMEI(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"somentei_mei": valor}:
                self.tem_somentei_mei = True
                self.valor = valor
            case _:
                self.tem_somentei_mei = False

    def filtrar(self, query):
        if self.tem_somentei_mei:
            condicional = Estabelecimento.empresa.has(
                Empresa.mei.has(MEI.mei == self.valor)
            )
            return query.where(condicional)
        return query


class FiltroSomenteMatriz(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"somente_matriz": valor}:
                self.tem_somente_matriz = True
                self.valor = valor
            case _:
                self.tem_somente_matriz = False

    def filtrar(self, query):
        if self.tem_somente_matriz:
            condicional = Estabelecimento.matriz_filial == self.valor
            return query.where(condicional)
        return query


class FiltroComTelefone(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"com_contato_telefonico": _}:
                self.tem_com_contato_telefonico = True
            case _:
                self.tem_com_contato_telefonico = False

    def filtrar(self, query):
        if self.tem_com_contato_telefonico:
            condicional = Estabelecimento.telefone_1.is_not(None)
            return query.where(condicional)
        return query


class FiltroComEmail(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"com_email": _}:
                self.tem_com_email = True
            case _:
                self.tem_com_email = False

    def filtrar(self, query):
        if self.tem_com_email:
            condicional = Estabelecimento.email.is_not(None)
            return query.where(condicional)
        return query


class FiltroSomenteFilial(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"somente_filial": valor}:
                self.tem_somente_filial = True
                self.valor = valor
            case _:
                self.tem_somente_filial = False

    def filtrar(self, query):
        if self.tem_somente_filial:
            condicional = Estabelecimento.matriz_filial == self.valor
            return query.where(condicional)
        return query


class FiltroExcluirMEI(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"excluir_mei": valor}:
                self.tem_excluir_mei = True
                self.valor = valor
            case _:
                self.tem_excluir_mei = False

    def filtrar(self, query):
        if self.tem_excluir_mei:
            condicional = Estabelecimento.empresa.has(
                Empresa.mei.has(MEI.mei.is_not(self.valor))
            )
            return query.where(condicional)
        return query


class FiltroSoCelular(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"somente_celular": valor}:
                self.tem_somente_celular = True
                self.valor = valor
            case _:
                self.tem_somente_celular = False

    def filtrar(self, query):
        if self.tem_somente_celular:
            condicional = or_(
                Estabelecimento.tipo_de_telefone_1 == self.valor,
                Estabelecimento.tipo_de_telefone_2 == self.valor,
            )
            return query.where(condicional)
        return query


class FiltroSoFixo(Filtro):
    def __init__(self, dados_formulario):
        match dados_formulario:
            case {"somente_fixo": valor}:
                self.tem_somente_fixo = True
                self.valor = valor
            case _:
                self.tem_somente_fixo = False

    def filtrar(self, query):
        if self.tem_somente_fixo:
            condicional = or_(
                Estabelecimento.tipo_de_telefone_1 == self.valor,
                Estabelecimento.tipo_de_telefone_2 == self.valor,
            )
            return query.where(condicional)
        return query


lista_de_filtros = [
    FiltroAtividades,
    FiltroBairro,
    FiltroCapitalSocial,
    FiltroCEP,
    FiltroComTelefone,
    FiltroComEmail,
    FiltroDataDeAbertura,
    FiltroDDD,
    FiltroExcluirMEI,
    FiltroMunicipio,
    FiltroSomenteMatriz,
    FiltroSoCelular,
    FiltroSoFixo,
    FiltroTermo,
    FiltroSituacaoCadastral,
    FiltroSomenteFilial,
    FiltroUF,
    FiltroNaturezaJuridica,
    FiltroSomenteMEI,
]

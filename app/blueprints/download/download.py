from flask import session, send_file
from app.objetos.requisição import Requisição
from .funcs.operador import Scav

def rota_download(blueprint):
    @blueprint.route("/download")
    def download():
        try:
            if session.get("_requisição"):
                req = Requisição(**session.get("_requisição"))
            else:
                req = Requisição()
            scav = Scav(req)
            scav.exportar_os_dados()
            return send_file("..\\static\\planilha.xlsx")
        except Exception as e:
            print(e)
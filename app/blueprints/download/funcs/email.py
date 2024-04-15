import smtplib
from email.message import EmailMessage
from os import getenv, remove
from pathlib import Path

from app.ext.fila import fila


def montar_email(email_destinatario: str) -> EmailMessage:
    corpo = """Você está recebendo a planilha com as informações solicitadas na plataforma do Scav.\n\nQualquer problema com o envio das informações ou dúvida, basta responder este email."""
    msg = EmailMessage()
    msg["subject"] = "Seus dados chegaram!"
    msg["From"] = getenv("SCAV_EMAIL")
    msg["To"] = email_destinatario
    msg.set_content(corpo)
    return msg


def enviar_mensagem(msg: EmailMessage, senha: str) -> None:
    s = smtplib.SMTP("smtp.office365.com", port=587)
    s.starttls()
    s.login(msg["From"], senha)
    s.send_message(msg)


def pegar_binario_planilha(caminho: str):
    with open(caminho, "rb") as f:
        dados = f.read()
    remove(caminho)
    return dados


@fila.task
def enviar_email(email_destinatario: str, file_name: str):
    print(f"Pedido de envio de planilha para {email_destinatario}")
    msg = montar_email(email_destinatario)
    senha = getenv("SCAV_SENHA")
    caminho = Path("./static") / file_name
    dados = pegar_binario_planilha(caminho)
    msg.add_attachment(
        dados,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="planilha.xlsx",
    )
    try:
        enviar_mensagem(msg, senha)
        print(f"Email enviado com sucesso para {msg['To']}")
    except Exception as e:
        print(e)
        raise e
    else:
        return f"Email enviado com sucesso para {msg['To']}"

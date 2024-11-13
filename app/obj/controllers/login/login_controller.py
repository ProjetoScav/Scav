from flask_sqlalchemy import SQLAlchemy

from app.ext.bcrypt import bcrypt
from app.ext.db.models import User
from app.obj.classes import LoginPopupMessages

MAX_LEN_PASSWORD = 20
MIN_LEN_PASSWORD = 8
MAX_LEN_NAME = 50


class LoginController:
    def __init__(self, db: SQLAlchemy) -> None:
        """Método __init__ de LoginController.

        Args:
            db (SQLAlchemy): proxy da db do SQLAlchemy

        """
        self.db = db
        self.messages = LoginPopupMessages()

    @staticmethod
    def get_register_form_data(form: dict[str, str]) -> tuple[str, str, str]:
        """Método que pega os dados de registro do formulário.

        Args:
            form (dict[str, str]): dados de registro enviados pelo usuário

        Returns:
            tuple[str, str, str]: retorno de email, name, password

        """
        email = form.get("account_email")
        name = form.get("account_name")
        password = form.get("account_email")
        return email, name, password

    @staticmethod
    def get_login_form_data(form: dict[str, str]) -> tuple[str, str]:
        """Método que pega os dados de login do formulário.

        Args:
            form (dict[str, str]): dados de login enviados pelo usuário

        Returns:
            tuple[str, str]: retorno de email, password

        """
        email = form.get("login-email")
        password = form.get("login-password")
        return email, password

    def validate_register(self, form: dict[str, str]) -> None:
        """Método que válida os registros de conta.

        Args:
            form (dict[str, str]): dados de registro enviados pelo usuário

        Returns:
            bool: validez do registro

        """
        email, name, password = self.get_register_form_data(form)
        user = self.db.session.query(User).filter(User.email == email).scalar()
        if user:
            self.messages.register_email.append("* Email já cadastrado")
        if len(password) > MAX_LEN_PASSWORD or len(password) < MIN_LEN_PASSWORD:
            self.messages.register_password = (
                "* Sua senha precisa ter entre 8 e 20 caracteres"
            )
        if len(name) > MAX_LEN_NAME:
            self.messages.register_name = (
                "* Seu nome não pode ultrapassar 50 caracteres"
            )
        return self.messages.validate_register()

    def register_user(self, form: dict[str, str]) -> User:
        """Método de registro de usuário.

        Args:
            form (dict[str, str]): dados de registro enviados pelo usuário

        Returns:
            User: o objeto do novo usuário

        """
        email, name, password = self.get_register_form_data(form)
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(email=email, name=name, password=hashed_password)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def validate_login(self, form: dict[str, str]) -> bool:
        """_summary_.

        Args:
            form (dict[str, str]): dados de login enviados pelo usuário

        Returns:
            bool: validez do login

        """
        email, password = self.get_login_form_data(form)
        user = self.db.session.query(User).filter(User.email == email).scalar()
        if not user:
            self.messages.invalid_login = "* E-mail e/ou senha inválidos"
        if not bcrypt.check_password_hash(user.password, password):
            self.messages.invalid_login = "* E-mail e/ou senha inválidos"
        return self.messages.validate_login()

from flask_sqlalchemy import SQLAlchemy

from app.ext.bcrypt import bcrypt
from app.ext.db.models import User
from app.obj.classes import LoginErrorMessages, RegisterErrorMessages

MAX_LEN_PASSWORD = 20
MIN_LEN_PASSWORD = 8
MAX_LEN_NAME = 50


class LoginController:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
        self.messages = {"name": "", "email": [], "login": "", "password": []}

    @staticmethod
    def get_register_form_data(form: dict[str, str]) -> tuple[str, str, str]:
        """Função que retira os dados de registro.

        Args:
            form (dict[str, str]): _description_

        Returns:
            tuple[str, str, str]: _description_

        """
        email = form.get("account_email")
        name = form.get("account_name")
        password = form.get("account_email")
        return email, name, password

    @staticmethod
    def get_login_form_data(form: dict[str, str]) -> tuple[str, str]:
        email = form.get("login-email")
        password = form.get("login-password")
        return email, password

    def validate_register(self, form: dict[str, str]) -> bool:
        validated = True
        email, name, password = self.get_register_form_data(form)
        user = self.db.session.query(User).filter(User.email == email).scalar()

        if user:
            self.messages["password"].append("* Email já cadastrado")
            validated = False

        if len(password) > MAX_LEN_PASSWORD or len(password) < MIN_LEN_PASSWORD:
            self.messages["password"].append(
                "* Sua senha precisa ter entre 8 e 20 caracteres"
            )
            validated = False

        if len(name) > MAX_LEN_NAME:
            self.messages["name"] = "* Seu nome não pode ultrapassar 50 caracteres"
            validated = False

        return validated

    def register_user(self, form: dict[str, str]) -> User:
        email, name, password = self.get_register_form_data(form)
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(email=email, name=name, password=hashed_password)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def validate_login(self, form: dict[str, str]) -> bool:
        email, password = self.get_login_form_data(form)
        user = self.db.session.query(User).filter(User.email == email).scalar()
        if not user:
            self.messages["login"] = "* E-mail e/ou senha inválidos"
            return False

        if bcrypt.check_password_hash(user.password, password):
            self.messages["login"] = "* E-mail e/ou senha inválidos"
            return False

        return True

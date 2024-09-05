from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from app.ext.db.db import db
from app.ext.db.models import User
from app.obj.controllers.login.login_controller import LoginController


def login_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Login
    no Blueprint"""

    @bp.route("/signup", methods=["POST", "GET"])
    def signup():
        login = LoginController(db)
        if login.validate_register(request.form):
            new_user = LoginController(db).register_user(request.form)
            login_user(new_user)
            return render_template("pages/logged_area.j2", user=new_user)
        return render_template(
            "components/forms/login_form.j2", messages=login.messages
        )

    @bp.route("/logged_area", methods=["GET"])
    @login_required
    def logged_area():
        return render_template("pages/logged_area.j2")

    @bp.route("/login/", methods=["POST", "GET"])
    def login():
        login = LoginController(db)
        if login.validate_login(request.form):
            user = (
                db.session.query(User)
                .filter(User.email == request.form.get("login-email"))
                .scalar()
            )
            login_user(user)
            return redirect(url_for("login.logged_area"))
        return render_template(
            "components/forms/register_form.j2", messages=login.messages
        )

    @bp.route("/logout", methods=["GET"])
    @login_required
    def logout():
        session.pop("query", None)
        logout_user()
        return redirect(url_for("home.home"))

    return bp

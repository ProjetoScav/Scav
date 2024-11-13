from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required, login_user, logout_user
from jinja2_fragments.flask import render_block

from app.ext.db.db import db
from app.ext.db.models import User
from app.obj.controllers.login.login_controller import LoginController


def login_routes(bp: Blueprint) -> Blueprint:
    """Função que registra as rotas de Login no Blueprint."""

    @bp.route("/signup", methods=["POST", "GET"])
    def signup():
        login = LoginController(db)
        if login.validate_register(request.form):
            new_user = LoginController(db).register_user(request.form)
            login_user(new_user)
            response = make_response("")
            response.headers["HX-Redirect"] = "/user_area"
            return response
        return render_block(
            "components/login-popup.j2",
            block_name="register_form",
            messages=login.messages,
        )

    @bp.route("/user_area", methods=["GET"])
    @login_required
    def user_area():
        return render_template("pages/user_area.j2")

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
            return redirect(url_for("login.user_area"))
        return render_block(
            "components/login-popup.j2",
            block_name="login_form",
            messages=login.messages,
        )

    @bp.route("/logout", methods=["GET"])
    @login_required
    def logout():
        session.pop("query", None)
        logout_user()
        return redirect(url_for("home.home"))

    return bp

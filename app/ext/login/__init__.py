from flask_login import LoginManager

from app.ext.db.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)

import os
from flask_wtf import CSRFProtect


def configurações(app):
    app.config["SECRET_KEY"] = os.urandom(20).hex()
    CSRFProtect(app)

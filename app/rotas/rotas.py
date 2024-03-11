from flask.templating import render_template
from flask import request

def configure(app):
    @app.route("/")
    def home():
        return render_template("index.html")

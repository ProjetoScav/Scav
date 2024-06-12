from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


db: SQLAlchemy = SQLAlchemy(model_class=Base)

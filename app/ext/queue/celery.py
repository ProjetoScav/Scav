from os import getenv

from celery import Celery
from dotenv import load_dotenv

load_dotenv(".flaskenv")
fila: Celery = Celery(
    "tasks",
    broker=getenv("REDIS_URL"),
    backend=getenv("REDIS_URL"),
)

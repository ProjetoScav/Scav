from os import getenv
from dotenv import load_dotenv
from celery import Celery

load_dotenv(".flaskenv")
fila = Celery(
    "tasks",
    broker=getenv("REDIS_URL"),
    backend=getenv("REDIS_URL"),
)
fila.config_from_object({"CELERY_ACCEPT_CONTENT": ["pickle", "json"]})

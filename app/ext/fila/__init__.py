from os import getenv
from dotenv import load_dotenv
from celery import Celery

load_dotenv(".flaskenv")
fila = Celery(
    "tasks",
    broker=getenv("REDIS_URL"),
    backend=getenv("REDIS_URL"),
)
fila.config_from_object(
    {"accept_content": ["pickle", "json"], "broker_connection_retry_on_startup": True}
)

from os import getenv

from celery import Celery

fila = Celery(
    "tasks",
    broker=getenv("REDIS_URL"),
    backend=getenv("REDIS_URL"),
)

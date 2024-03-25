from flask.app import Flask
from .blueprints import configurar_blueprints
from .config import configurações
from .extensions import cache, configurar_extensões
# from celery import Celery, Task

# class FlaskTask(Task)

#     def __call__(self, *args: object, **kwargs: object) -> object:
#         with self.__app.app_context():
#             return self.run(*args, **kwargs)

# def celery_init_app(app: Flask) -> Celery:
#     print(FlaskTask(app))
#     celery_app = Celery(app.name, task_cls=FlaskTask(app))
#     celery_app.config_from_object(app.config["CELERY"])
#     celery_app.set_default()
#     app.extensions["celery"] = celery_app
    # celery_app.Task = FlaskTask
#     return celery_app


def create_app():
    app = Flask(
        __name__,
        static_folder="../static/",
    )
    # app.config.from_mapping(
    #     CELERY=dict(
    #         broker_url="pyamqp://guest@localhost",
    #         task_ignore_result=True,
    #     ),
    # )
    cache.init_app(app, config={"CACHE_TYPE": "simple"})
    # celery_init_app(app)
    configurações(app)
    configurar_blueprints(app)
    configurar_extensões(app)
    return app

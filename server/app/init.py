from flask import Flask
from celery import Celery
app = Flask(__name__)
celery = Celery(
    app.import_name,
    backend='redis://localhost:6379/1',
    broker='redis://localhost:6379/0'
    # backend='redis://192.168.31.10:6379/1',
    # broker='redis://192.168.31.10:6379/0'
)
celery.conf.timezone = "Asia/Shanghai"


def init_app():
    from .views import register_blueprint

    register_blueprint(app)
    return app

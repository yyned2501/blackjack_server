from flask import Flask
from celery import Celery
import redis
app = Flask(__name__)
celery = Celery(
    app.import_name,
    backend="redis://localhost:6379/1",
    broker="redis://localhost:6379/0",
)
celery.conf.timezone = "Asia/Shanghai"

redis_cli = redis.Redis(host="localhost", port=6379, db=2)

def init_app():
    from .views import register_blueprint

    register_blueprint(app)
    return app

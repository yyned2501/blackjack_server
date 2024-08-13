from flask import Flask
# from .api import app as api


def register_blueprint(app: Flask):
    from .index import index

    # app.register_blueprint(api, url_prefix="/api")

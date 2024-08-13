from flask import Flask
from .api import app as api
from .web import app as web



def register_blueprint(app: Flask):
    # from .index import index

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(web, url_prefix="/web")

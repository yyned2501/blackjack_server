import json
import time

from flask import render_template, request, Blueprint
from .api import states
from app.libs import celery_tasks
from app.init import redis_cli

app = Blueprint("web", __name__)


@app.route("/state")
def state():
    return render_template("state.html", states=states)

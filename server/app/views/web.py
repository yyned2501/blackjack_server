import copy
import datetime

from flask import render_template, Blueprint

from .api import states

app = Blueprint("web", __name__)


@app.route("/state")
def state():
    _states = copy.deepcopy(states)
    _states["next_ts"] = datetime.datetime.fromtimestamp(
        _states.get("next_time", 0)
    ).strftime("%Y-%m-%d %H:%M:%S")
    _states["update_ts"] = datetime.datetime.fromtimestamp(
        _states.get("update_time", 0)
    ).strftime("%Y-%m-%d %H:%M:%S")
    return render_template("state.html", states=states)

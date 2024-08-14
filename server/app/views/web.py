import copy
import datetime

from flask import render_template, Blueprint

from .api import states

app = Blueprint("web", __name__)


@app.route("/state")
def state():
    _states = copy.deepcopy({k: states[k] for k in sorted(states)})
    for _, state in _states.items():
        state["next_ts"] = datetime.datetime.fromtimestamp(
            state.get("next_time", 0)
        ).strftime("%Y-%m-%d %H:%M:%S")
        state["update_ts"] = datetime.datetime.fromtimestamp(
            state.get("update_time", 0)
        ).strftime("%Y-%m-%d %H:%M:%S")
    return render_template("state.html", states=_states)

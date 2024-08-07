import datetime
from app.init import app
from flask import request, jsonify
import time

states = {'31341': {'next_date': '2024-08-07 18:31:17', 'next_time': 1723026677, 'point': 21, 'sleep': 89, 'state': 1, 'userid': 31341}, '36916': {'next_date': '2024-08-07 18:30:03', 'next_time': 1723026603, 'sleep': 11, 'state': 1, 'userid': 36916}, '39819': {'next_date': '2024-08-07 18:31:16', 'next_time': 1723026676, 'point': 21, 'sleep': 111, 'state': 1, 'userid': 39819}, '40074': {'next_date': '2024-08-07 18:31:12', 'next_time': 1723026672, 'sleep': 101, 'state': 1, 'userid': 40074}}
states = {}

def delete_old_states():
    for k in list(states.keys()):
        if time.time() - states[k]["next_time"] > 20:
            del states[k]


@app.route("/", methods=["POST"])
def index():
    state = {}
    for k, v in request.form.lists():
        v = v[0]
        try:
            state[k] = int(v)
        except ValueError:
            state[k] = v
    if "sleep" in state:
        state["next_time"] = int(time.time()) + state["sleep"]
    state["next_date"] = datetime.datetime.fromtimestamp(state["next_time"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    states[state["userid"]] = state
    delete_old_states()
    return jsonify(states)


@app.route("/", methods=["GET"])
def index_():
    delete_old_states()
    return jsonify(states)


@app.route("/api/states", methods=["POST"])
def api_states():
    data = request.form.getlist("data")
    for k in states:
        if str(k) in data:
            states[k]["state"] = 1
        else:
            if "state" in states[k]:
                del states[k]["state"]
    return jsonify(states)

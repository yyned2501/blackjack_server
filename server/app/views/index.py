from app.init import app, redis_cli
from flask import request, jsonify
import json
import time
from app.libs import celery_tasks

states = {}


def delete_old_states():
    for k in list(states.keys()):
        if time.time() - states[k]["next_time"] - states[k].get("sleep", 120) * 2 > 20:
            del states[k]
            celery_tasks.tg_message.delay(f"客户端{k}已离线")


@app.route("/api/state", methods=["POST"])
def index():
    state = {}
    for k, v in request.form.lists():
        v = v[0]
        try:
            state[k] = int(v)
        except ValueError:
            state[k] = v
    state["update_time"] = int(time.time())

    if "sleep" in state:
        state["next_time"] = int(time.time()) + state["sleep"]

    if (point := state.get("point")) and (point <= 21):
        celery_tasks.tg_state.delay(state)

    states[state["userid"]] = state
    redis_cli.set(state["userid"], json.dumps(state))
    return jsonify(states)


@app.route("/api/state", methods=["GET"])
def index_():
    delete_old_states()
    return jsonify(states)


@app.route("/api/states", methods=["POST"])
def api_states():
    data = request.form.getlist("data")
    user_id = request.form.get("userid", None)
    sleep = int(request.form.get("sleep", 20))

    if user_id:
        user_id = int(user_id)
        if user_id not in states:
            state = (
                json.loads(state_json)
                if (state_json := redis_cli.get(user_id))
                else {"userid": user_id, "sleep": sleep}
            )
            states[user_id] = state
            if (
                time.time() - state.get("next_time", 0) - state.get("sleep", 120) * 2
                > 20
            ):
                celery_tasks.tg_message.delay(f"客户端{user_id}恢复链接")

        state = states[user_id]
        state["next_time"] = int(time.time()) + state["sleep"]

    for k in states:
        if str(k) in data:
            states[k]["state"] = 1
        else:
            if states[k].get("state"):
                if time.time() - states[k].get("update_time", 0) > 5:
                    del states[k]["state"]

    return jsonify(states)

import datetime
from app.init import app
from flask import request, jsonify
import time
from app.libs import celery_tasks
states = {}


def delete_old_states():
    for k in list(states.keys()):
        if time.time() - states[k]["next_time"] - states[k].get("sleep", 0) * 2 > 20:
            del states[k]
            celery_tasks.tg_message(f"客户端{k}已离线")


# @app.route("/", methods=["POST"])
@app.route("/api/state", methods=["POST"])
def index():
    state = {}
    for k, v in request.form.lists():
        v = v[0]
        try:
            state[k] = int(v)
        except ValueError:
            state[k] = v
    state["update_date"] = datetime.datetime.fromtimestamp(int(time.time())).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    if "sleep" in state:
        state["next_time"] = int(time.time()) + state["sleep"]
    state["next_date"] = datetime.datetime.fromtimestamp(state["next_time"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    if (point := state.get("point")) and (point <= 21):
        celery_tasks.tg_message.delay(
            f'{state.get("userid")}开始钓鱼，点数{point}，魔力{state.get("bonus","未知")}')
    states[state["userid"]] = state
    delete_old_states()
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
            state = {"userid": user_id, "sleep": sleep}
            states[user_id] = state
        state = states[user_id]
        state["next_time"] = int(time.time()) + state["sleep"]
        state["next_date"] = datetime.datetime.fromtimestamp(
            state["next_time"]
        ).strftime("%Y-%m-%d %H:%M:%S")

    for k in states:
        if str(k) in data:
            states[k]["state"] = 1
        else:
            if "state" in states[k]:
                del states[k]["state"]

    return jsonify(states)


@app.route("/api/test", methods=["GET"])
def test():
    celery_tasks.tg_message.delay("测试并发推送")
    return "OK"

import json
from app.init import celery, redis_cli
from app.libs import tgbot


@celery.task
def tg_message(content: str):
    return tgbot.telegram_bot(content)


@celery.task
def tg_state(state: dict):
    if state_json := redis_cli.get(state.get("userid")):
        state_last: dict = json.loads(state_json)
    if state.get("update_time") == state_last.get("update_time"):
        return "已推送防抖"
    return tgbot.telegram_bot(
        f'{state.get("userid")}开始钓鱼，点数{state.get("point","未知")}，魔力{state.get("bonus","未知")}'
    )

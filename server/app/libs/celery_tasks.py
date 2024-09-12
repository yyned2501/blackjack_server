import json
from app.init import celery, redis_cli
from app.libs import tgbot


@celery.task
def tg_message(content: str):
    return tgbot.telegram_bot(content)


@celery.task
def tg_state(state: dict):
    model = "自助" if state.get("gift_model") else "钓鱼"
    return tgbot.telegram_bot(
        f'{state.get("userid")}开始{model}，点数{state.get("point","未知")}，魔力{state.get("bonus","未知")}，下载量{state.get("downloads","未知")}'
    )

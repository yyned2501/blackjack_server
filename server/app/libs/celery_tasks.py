import json
from app.init import celery, redis_cli
from app.libs import tgbot


@celery.task
def tg_message(content: str):
    return tgbot.telegram_bot(content)


@celery.task
def tg_state(state: dict):
    return tgbot.telegram_bot(
        f'{state.get("userid")}开始{'赠送' if state.get("gift_model") else '钓鱼'}，点数{state.get("point","未知")}，魔力{state.get("bonus","未知")}，下载量{state.get("downloads","未知")}'
    )

from app.init import celery
from app.libs import tgbot


@celery.task
def tg_message(content: str):
    return tgbot.telegram_bot(content)


@celery.task
def tg_state(state: dict):
    print(state)
    return tgbot.telegram_bot(
        f'{state.get("userid")}开始钓鱼，点数{state.get("point","未知")}，魔力{state.get("bonus","未知")}'
    )

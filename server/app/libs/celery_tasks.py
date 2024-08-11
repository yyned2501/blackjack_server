from app.init import celery
from app.libs import tgbot


@celery.task
def tg_message(content: str):
    tgbot.telegram_bot(content)

import requests


push_config = {
    "TG_BOT_TOKEN": "6813515442:AAEjwNe041aBe8p9E6Fm2BTygixJMBpzqKU",
    "TG_USER_ID": "-1002238339105",  # tg 机器人的 TG_USER_ID，例：1434078534
}


def telegram_bot(content: str) -> None:
    url = f"https://api.telegram.org/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "chat_id": str(push_config.get("TG_USER_ID")),
        "text": f"{content}",
        "disable_web_page_preview": "true",
    }

    response = requests.post(url=url, headers=headers, params=payload).json()

    return response


if __name__ == "__main__":
    telegram_bot("机器人推送测试")

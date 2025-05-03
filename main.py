import requests
from telegram import Bot
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADDRESS = "0xb39115d0b712753614a726897f0e74Bd2518f34"  # активна адреса з Explorer

bot = Bot(token=TOKEN)

def get_btcc_price():
    try:
        url = "https://scan.bitcoincode.technology/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": ADDRESS,
            "sort": "desc"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "result" not in data or not data["result"]:
            return "❌ GraphQL: транзакції не знайдено"

        last_tx = data["result"][0]
        value = int(last_tx["value"])
        btcc_amount = value / 1e18  # токени в форматі wei

        return f"{btcc_amount:.8f} BTCC"

    except Exception as e:
        return f"❌ Помилка: {str(e)}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🧠 GraphQL API активний — Танішка спостерігає за ринком BTCC 🌺")
    while True:
        send_price()
        time.sleep(300)

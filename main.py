import requests
from telegram import Bot
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADDRESS = "0xb39115d0b712753614a726897f0e74Bd2518f34"

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

        # Перевірка на успішність
        if data.get("status") != "1" or "result" not in data or not data["result"]:
            return "❌ Поточна ціна BTCC: Транзакції не знайдено"

        # Проходимось по транзакціях, знаходимо першу з value > 0
        for tx in data["result"]:
            if tx.get("isError") == "0" and tx.get("value") and int(tx["value"]) > 0:
                value_wei = int(tx["value"])
                value_btcc = value_wei / 1e18
                return f"{value_btcc:.8f} BTCC"

        return "❌ Поточна ціна BTCC: Немає валідних транзакцій"

    except Exception as e:
        return f"❌ Поточна ціна BTCC: Помилка — {str(e)}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🧠 GraphQL API активний — Танішка спостерігає за ринком BTCC 🌸")
    while True:
        send_price()
        time.sleep(300)
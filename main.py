import requests
from telegram import Bot
import os
import time

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADDRESS = "0x3B9115d0b712753614a726879F0e74Bd2518f34"  # адреса з активними свапами

bot = Bot(token=TOKEN)

def get_btcc_price():
    try:
        url = "https://scan.bitcoincode.technology/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": ADDRESS,
            "sort": "desc",
            "page": 1,
            "offset": 25
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "result" not in data or not data["result"]:
            return "❌ Поточна ціна BTCC: Транзакцій не знайдено"

        # Проходимо по транзакціях і шукаємо SwapTokensForExactETH з value > 0
        for tx in data["result"]:
            method = tx.get("functionName", "")
            value = int(tx.get("value", "0"))

            if "SwapTokensForExactETH" in method and value > 0:
                btcc = value / 10**18
                return f"📉 Поточна ціна BTCC: {btcc:.8f} BTCC"

        return "❌ Поточна ціна BTCC: Немає актуальних обмінів"
    except Exception as e:
        return f"❌ Помилка: {str(e)}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=price)

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 GraphQL API активний — Танішка спостерігає за ринком BTCC 🌺")
    while True:
        send_price()
        time.sleep(30)
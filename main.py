import requests
import os
import time
from datetime import datetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADDRESS = "0x3B9115d0b712753614a726879F0e74Bd2518f34".lower()
API_URL = f"https://scan.bitcoincode.technology/api?module=account&action=txlist&address={ADDRESS}&sort=desc&page=1&offset=1"

bot = Bot(token=TOKEN)

def get_btcc_price():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if data.get("status") != "1" or not data.get("result"):
            return "❌ Поточна ціна BTCC: Транзакцій не знайдено 😢"

        tx = data["result"][0]
        value = int(tx["value"]) / 10**18
        tx_time = datetime.fromtimestamp(int(tx["timeStamp"])).strftime("%Y-%m-%d %H:%M:%S")
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            f"📊 Поточна ціна BTCC: {value:.6f} BTCC\n"
            f"🕒 Час транзакції: {tx_time}\n"
            f"📬 Надіслано: {now_time}"
        )
    except Exception as e:
        return f"❌ Помилка: {str(e)}"

def send_price():
    text = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 API активний — Танішка стежить за BTCC 💞")
    while True:
        send_price()
        time.sleep(6000000)

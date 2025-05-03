import requests
from telegram import Bot
from telegram.error import TelegramError
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADDRESS = "0x3B9115d0b712753614a726879F0e74Bd2518f34"
API_URL = f"https://scan.bitcoincode.technology/api?module=account&action=txlist&address={ADDRESS}&sort=desc&page=1&offset=1"

bot = Bot(token=TOKEN)

def get_latest_btcc_transaction():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if "result" not in data or not data["result"]:
            return "❌ Поточна ціна BTCC: Транзакцій не знайдено"

        tx = data["result"][0]
        value = int(tx["value"]) / 10**18
        return f"📉 Поточна ціна BTCC: {value:.10f} BTCC"

    except Exception as e:
        return f"❌ GraphQL API помилка: {str(e)}"

def main():
    while True:
        try:
            text = get_latest_btcc_transaction()
            bot.send_message(chat_id=CHAT_ID, text=text)
        except TelegramError as e:
            print(f"Telegram error: {e}")
        except Exception as e:
            print(f"Unhandled error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()

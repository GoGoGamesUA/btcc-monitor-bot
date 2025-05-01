import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://swap.bitcoincode.technology/#/overview"

bot = Bot(token=TOKEN)

def get_btcc_price():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знаходимо span, який містить "$" і цифри — це точний селектор
        price_element = soup.find("span", string=lambda text: text and "$" in text and any(char.isdigit() for char in text))

        if price_element:
            return price_element.text.strip()
        else:
            return "❌ Ціну не знайдено"
    except Exception as e:
        print("Error:", e)
        return "❌ Помилка при парсингу"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 Ціна BTCC під контролем. Танішка не спить 😎")
    while True:
        send_price()
        time.sleep(300)

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
        response = requests.get("https://swap.bitcoincode.technology/#/overview", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знаходимо span з точною назвою класу
        price_tag = soup.find("span", class_="sc-fyjhYU jGQVVX")
        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return "❌ Ціну не знайдено"
    except Exception as e:
        return f"❌ Помилка: {e}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 Ціна BTCC під контролем. Танішка не спить 😎")
    while True:
        send_price()
        time.sleep(300)

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
        
        # Знайдемо елемент з ціною (тицьнемо пальцем по HTML-структурі)
        price_div = soup.find("div", string="BTCC Price")
        if price_div:
            parent = price_div.find_parent()
            price = parent.find_all("div")[1].text.strip()
            return price
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
        time.sleep(300)  # кожні 5 хвилин

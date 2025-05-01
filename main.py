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
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Шукаємо блок з назвою "BTCC Price"
        label_div = soup.find('div', string=lambda s: s and 'BTCC Price' in s)
        if label_div:
            # Беремо наступний <span> після нього
            price_span = label_div.find_next('span')
            if price_span:
                return price_span.text.strip()

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

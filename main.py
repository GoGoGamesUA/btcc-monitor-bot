import os
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://swap.bitcoincode.technology/#/overview"

bot = Bot(token=TOKEN)

def get_btcc_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        price_div = soup.find("div", string="BTCC Price")
        if price_div:
            parent = price_div.find_parent()
            price = parent.find_all("div")[1].text.strip()
            return price
        else:
            return "❌ Ціну не знайдено"
    except Exception as e:
        print("Помилка при парсингу:", e)
        return "❌ Помилка при парсингу"

async def send_price():
    price = get_btcc_price()
    await bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="🔍 Ціна BTCC під контролем. Танішка не спить 😎")
    while True:
        await send_price()
        await asyncio.sleep(300)  # кожні 5 хв

if __name__ == "__main__":
    asyncio.run(main())

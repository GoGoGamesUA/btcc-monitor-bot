from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telegram import Bot
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://swap.bitcoincode.technology/#/overview"
CHROME_PATH = "./chromedriver.exe"

bot = Bot(token=TOKEN)

def get_btcc_price():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    time.sleep(5)

    try:
        price_element = driver.find_element(By.XPATH, "//div[contains(text(),'BTCC Price')]/following-sibling::div")
        price = price_element.text.strip()
    except Exception as e:
        price = "❌ Ціну не знайдено"
        print("Error:", e)

    driver.quit()
    return price

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 Ціна BTCC під контролем. Танішка не спить 😎")
    while True:
        send_price()
        time.sleep(300)  # кожні 5 хвилин

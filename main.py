import requests
from telegram import Bot
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GRAPHQL_URL = "https://scan.bitcoincode.technology/graphql"

bot = Bot(token=TOKEN)

def get_btcc_price():
    query = """
    {
      transactions(first: 10, orderBy: timestamp, orderDirection: desc) {
        method
        tokenTransfers {
          tokenSymbol
          amount
        }
      }
    }
    """
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)

        # Перевірка, чи сервер взагалі відповів
        if response.status_code != 200:
            return f"❌ GraphQL помилка: HTTP {response.status_code}"

        data = response.json()

        # Перевірка, чи в JSON є блок "data"
        if "data" not in data or "transactions" not in data["data"]:
            return "❌ GraphQL відповідь неправильна"

        for tx in data["data"]["transactions"]:
            if "SwapTokensForExactETH" in tx.get("method", ""):
                btcc = eth = None
                for t in tx.get("tokenTransfers", []):
                    if t["tokenSymbol"] == "BTCC":
                        btcc = float(t["amount"])
                    elif t["tokenSymbol"] == "ETH":
                        eth = float(t["amount"])
                if btcc and eth:
                    price = eth / btcc
                    return f"{price:.6f} ETH"
        return "❌ Ціну не знайдено у свопах"
    except Exception as e:
        return f"❌ Помилка: {e}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 GraphQL API активний — Танішка спостерігає за ринком BTCC 🌸")
    while True:
        send_price()
        time.sleep(300)  # Кожні 5 хвилин

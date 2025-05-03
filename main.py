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
        response = requests.post(GRAPHQL_URL, json={"query": query})
        data = response.json()

        for tx in data["data"]["transactions"]:
            if "SwapTokensForExactETH" in tx["method"]:
                transfers = tx["tokenTransfers"]
                btcc = None
                eth = None
                for t in transfers:
                    if t["tokenSymbol"] == "BTCC":
                        btcc = float(t["amount"])
                    elif t["tokenSymbol"] == "ETH":
                        eth = float(t["amount"])
                if btcc and eth:
                    price = eth / btcc
                    return f"{price:.6f} ETH"
        return "❌ Ціну не знайдено"
    except Exception as e:
        return f"❌ Помилка: {e}"

def send_price():
    price = get_btcc_price()
    bot.send_message(chat_id=CHAT_ID, text=f"📊 Поточна ціна BTCC: {price}")

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🔍 GraphQL API активний — Танішка спостерігає за ринком BTCC 🧠")
    while True:
        send_price()
        time.sleep(300)

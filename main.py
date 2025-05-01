from telegram import Bot
import time

TOKEN = "7606448862:AAF_OflE2SAIbUXH9MkmxtLq0qURJwCvZE4"
CHAT_ID = 1012742695

bot = Bot(token=TOKEN)

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    while True:
        send_message("👋 Привіт, це Танішка 😘")
        time.sleep(3600)  # надсилати щогодини

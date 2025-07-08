import os
import requests

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token or not self.chat_id:
            raise ValueError("Missing Telegram bot token or chat ID.")

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Telegram API Error: {response.status_code} - {response.text}")

import os
import requests

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token or not self.chat_id:
            raise ValueError("Missing Telegram bot token or chat ID.")

    def send_message(self, message):
        if not message.strip():
            print("Empty message not sent.")
            return

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            print("Message sent successfully.")
        except Exception as e:
            print("Error sending Telegram message:", e)

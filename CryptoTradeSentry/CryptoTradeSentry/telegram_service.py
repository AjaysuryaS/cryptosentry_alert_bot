import requests

BOT_TOKEN = "7258922131:AAEklzNSS-iXX6Lglkd_Wr7TA9q6mniW5M8"
CHAT_ID = "1970010422"

def send_telegram_message(message):
    if not message.strip():
        print("Empty message not sent.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("Message sent successfully.")
    except Exception as e:
        print("Error sending Telegram message:", e)

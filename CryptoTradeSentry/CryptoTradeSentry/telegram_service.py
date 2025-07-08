import requests
import logging

class TelegramService:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def update_config(self, bot_token, chat_id):
        """Update Telegram configuration"""
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def send_message(self, message):
        """Send message via Telegram bot"""
        if not self.bot_token or not self.chat_id:
            logging.error("Telegram bot token or chat ID not configured")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                logging.info(f"Telegram message sent successfully: {message}")
                return True
            else:
                logging.error(f"Telegram API error: {result}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending Telegram message: {str(e)}")
            return False
    
    def test_connection(self):
        """Test Telegram bot connection"""
        if not self.bot_token:
            return False, "Bot token not configured"
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                bot_info = result.get('result', {})
                return True, f"Connected to bot: {bot_info.get('first_name', 'Unknown')}"
            else:
                return False, f"Telegram API error: {result}"
                
        except Exception as e:
            return False, f"Connection error: {str(e)}"

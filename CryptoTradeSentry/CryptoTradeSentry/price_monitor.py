import requests
import time
import threading
import logging
from datetime import datetime
from app import app, db
from models import MonitorConfig, PriceAlert, PriceHistory
from telegram_service import TelegramService

class PriceMonitor:
    def __init__(self):
        self.running = False
        self.thread = None
        self.config = None
        self.telegram = TelegramService()
        self.last_notified = None
        self.update_config()
    
    def update_config(self):
        """Update configuration from database"""
        with app.app_context():
            self.config = MonitorConfig.query.first()
            if self.config:
                self.telegram.update_config(self.config.bot_token, self.config.chat_id)
    
    def get_xec_price(self):
        """Fetch current XEC/USDT price from CoinGecko Binance ticker API"""
        try:
            response = requests.get(
                'https://api.coingecko.com/api/v3/exchanges/binance/tickers?coin_ids=ecash',
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Find XEC/USDT ticker
            if 'tickers' in data:
                for ticker in data['tickers']:
                    if ticker.get('base') == 'XEC' and ticker.get('target') == 'USDT':
                        return float(ticker['last'])
            
            logging.error("XEC/USDT ticker not found in CoinGecko Binance response")
            return None
        except Exception as e:
            logging.error(f"Error fetching XEC price from CoinGecko Binance API: {str(e)}")
            return None
    
    def save_price_history(self, price):
        """Save price to database"""
        try:
            with app.app_context():
                price_record = PriceHistory(price=price)
                db.session.add(price_record)
                db.session.commit()
        except Exception as e:
            logging.error(f"Error saving price history: {str(e)}")
    
    def check_alerts(self, current_price):
        """Check if price crosses thresholds and send alerts"""
        if not self.config:
            return
        
        alert_sent = False
        
        # Check upper threshold
        if current_price > self.config.upper_threshold and self.last_notified != 'above_upper':
            message = f"🚀 XEC/USDT crossed {self.config.upper_threshold}! Current: {current_price:.8f}"
            success = self.telegram.send_message(message)
            
            with app.app_context():
                alert = PriceAlert(
                    price=current_price,
                    threshold=self.config.upper_threshold,
                    alert_type='above_upper',
                    message=message,
                    sent_successfully=success
                )
                if not success:
                    alert.error_message = "Failed to send Telegram message"
                db.session.add(alert)
                db.session.commit()
            
            if success:
                self.last_notified = 'above_upper'
                alert_sent = True
                logging.info(f"Upper threshold alert sent: {message}")
        
        # Check lower threshold
        elif current_price <= self.config.lower_threshold and self.last_notified != 'below_lower':
            message = f"🎯 XEC/USDT touched sniper retest zone {self.config.lower_threshold}! Current: {current_price:.8f}"
            success = self.telegram.send_message(message)
            
            with app.app_context():
                alert = PriceAlert(
                    price=current_price,
                    threshold=self.config.lower_threshold,
                    alert_type='below_lower',
                    message=message,
                    sent_successfully=success
                )
                if not success:
                    alert.error_message = "Failed to send Telegram message"
                db.session.add(alert)
                db.session.commit()
            
            if success:
                self.last_notified = 'below_lower'
                alert_sent = True
                logging.info(f"Lower threshold alert sent: {message}")
        
        # Reset notification state if price is between thresholds
        if self.config.lower_threshold < current_price < self.config.upper_threshold:
            self.last_notified = None
        
        return alert_sent
    
    def monitor_loop(self):
        """Main monitoring loop"""
        logging.info("Price monitoring loop started")
        
        while self.running:
            try:
                # Update configuration from database
                self.update_config()
                
                # Skip if monitoring is disabled
                if not self.config or not self.config.monitoring_enabled:
                    time.sleep(5)  # Check every 5 seconds for config changes
                    continue
                
                # Fetch current price
                current_price = self.get_xec_price()
                
                if current_price is not None:
                    # Save price to history
                    self.save_price_history(current_price)
                    
                    # Check for alerts
                    self.check_alerts(current_price)
                    
                    logging.debug(f"Current XEC price: {current_price:.8f}")
                else:
                    logging.warning("Failed to fetch current price")
                
                # Wait for next check
                sleep_time = self.config.check_interval if self.config else 30
                time.sleep(sleep_time)
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(30)  # Wait 30 seconds before retrying
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.thread.start()
            logging.info("Price monitoring started")
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logging.info("Price monitoring stopped")

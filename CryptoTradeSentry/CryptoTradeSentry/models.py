from app import db
from datetime import datetime

class MonitorConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_token = db.Column(db.String(256), nullable=False)
    chat_id = db.Column(db.String(64), nullable=False)
    upper_threshold = db.Column(db.Float, default=0.00001845)
    lower_threshold = db.Column(db.Float, default=0.00001830)
    monitoring_enabled = db.Column(db.Boolean, default=False)
    check_interval = db.Column(db.Integer, default=30)  # seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PriceAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(32), nullable=False)  # 'above_upper', 'below_lower'
    message = db.Column(db.Text, nullable=False)
    sent_successfully = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

from dotenv import load_dotenv
load_dotenv()  # ✅ Load .env variables FIRST

from app import app
import threading
import logging

# Add a simple health check route
@app.route('/health')
def health():
    return "✅ CryptoTradeSentry is alive and monitoring XEC/USDT"

if __name__ == '__main__':
    from price_monitor import PriceMonitor

    monitor = PriceMonitor()

    # Start price monitoring in a background thread
    monitor_thread = threading.Thread(target=monitor.start_monitoring, daemon=True)
    monitor_thread.start()
    logging.info("✅ Price monitoring thread started")

    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

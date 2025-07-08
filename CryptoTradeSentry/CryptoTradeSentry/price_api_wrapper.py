"""
Price API Wrapper - Provides Binance-style interface using CoinGecko backend for XEC/USDT
"""
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_xec_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ecash&vs_currencies=usd"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["ecash"]["usd"])
    except Exception as e:
        print("Error fetching price:", e)
        return None

def get_binance_style_response():
    """
    Get price in Binance API response format using CoinGecko backend
    """
    try:
        price = get_current_price()
        if price is not None:
            return {
                "symbol": "XECUSDT",
                "price": str(price)
            }
        else:
            return None
    except Exception as e:
        print("Error fetching price:", e)
        return None

# Test the wrapper
if __name__ == "__main__":
    print("Testing Price API Wrapper:")
    
    # Test simple price function
    price = get_current_price()
    if price:
        print(f"Current XEC/USDT: {price:.8f}")
    
    # Test Binance-style response
    response = get_binance_style_response()
    if response:
        print(f"Binance-style response: {response}")

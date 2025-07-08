"""
Price API Wrapper - Provides Binance-style interface using CoinGecko backend for XEC/USDT
"""
import requests

def get_current_price():
    """
    Get current XEC/USDT price using CoinGecko API
    Returns price in the same format as the Binance API would
    """
    url = "https://api.coingecko.com/api/v3/exchanges/binance/tickers?coin_ids=ecash"
    try:
        response = requests.get(url)
        data = response.json()
        tickers = data.get("tickers", [])
        for ticker in tickers:
            if ticker["base"] == "XEC" and ticker["target"] == "USDT":
                return float(ticker["last"])
    except Exception as e:
        print("Error fetching accurate price from CoinGecko Binance feed:", e)
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
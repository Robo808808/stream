import os
import yfinance as yf
import requests

ALPHA_API_KEY = os.environ.get("ALPHA_API_KEY")

def fetch_yf_fx():
    ticker = yf.Ticker("GBPUSD=X")
    data = ticker.history(period="1d", interval="1m")
    if data.empty:
        return None
    row = data.iloc[-1]
    return {
        "timestamp": row.name.to_pydatetime().isoformat(),
        "price": float(row["Close"])
    }

def fetch_alpha_fx():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "GBP",
        "to_currency": "USD",
        "apikey": ALPHA_API_KEY
    }
    r = requests.get(url, params=params)
    if not r.ok:
        return None
    result = r.json().get("Realtime Currency Exchange Rate", {})
    return {
        "timestamp": result.get("6. Last Refreshed"),
        "price": float(result.get("5. Exchange Rate"))
    } if "5. Exchange Rate" in result else None

def get_fx_price():
    from config import USE_REAL_MARKET_DATA
    return fetch_alpha_fx() if USE_REAL_MARKET_DATA else fetch_yf_fx()

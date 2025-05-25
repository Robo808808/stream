import os
import yfinance as yf
import requests
import time
from random import uniform
from datetime import datetime

ALPHA_API_KEY = os.environ.get("ALPHA_API_KEY")

def fetch_gbp_usd_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "price": round(uniform(1.345, 1.365), 5)  # simulate price jitter
    }

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
        "timestamp": datetime.now().isoformat(),
        "price": round(uniform(1.22, 1.28), 5)
    } if "5. Exchange Rate" in result else None

def get_fx_price():
    from config import USE_REAL_MARKET_DATA
    return fetch_alpha_fx() if USE_REAL_MARKET_DATA else fetch_yf_fx()

def retry_fetch(fetch_fn, retries=3, delay=2):
    for attempt in range(retries):
        result = fetch_fn()
        if result:
            return result
        print(f"⏳ Retry {attempt+1}/{retries} failed. Retrying in {delay}s...")
        time.sleep(delay)
    return None

def get_fx_price():
    from config import USE_REAL_MARKET_DATA, USE_SIMULATED_PRICES
    if USE_SIMULATED_PRICES:
        return retry_fetch(fetch_gbp_usd_data)

    fetch = fetch_alpha_fx if USE_REAL_MARKET_DATA else fetch_yf_fx
    return retry_fetch(fetch)


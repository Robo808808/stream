from strategies.simple_threshold import ThresholdStrategy
from trading.oanda_executor import execute_trade_oanda
from trading.executor import execute_trade
from trading.logger import log_trade
from marketdata.fetcher import get_fx_price
import yfinance as yf
import pandas as pd
import time

def fetch_gbp_usd_data():
    ticker = "GBPUSD=X"
    #data = yf.Ticker(ticker)
    data = get_fx_price()
    hist = data.history(period="1d", interval="1m")
    if not hist.empty:
        latest = hist.iloc[-1]
        return {
            "timestamp": latest.name,
            "price": latest["Close"]
        }
    return None

def stream_gbp_usd_data(strategy, interval=10):
    df = pd.DataFrame(columns=["timestamp", "price"])

    try:
        while True:
            data = fetch_gbp_usd_data()
            if data:
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                signal = strategy.evaluate(df)

                print(f"[{data['timestamp']}] Price: {data['price']:.4f} → Signal: {signal['action']}")
                if signal['action'] in ("BUY", "SELL"):
                    # 👉 plug into Alpha Vantage or broker API here
                    #response = execute_trade(signal['action'], signal['price'])
                    #print(f"✅ Trade Response: {response}")
                    #print(f"🔔 EXECUTE {signal['action']} @ {signal['price']}")
                    if LIVE_TRADING:
                        trade_response = execute_trade_oanda(signal['action'], signal['price'])
                    else:
                        trade_response = log_trade(signal['action'], signal['price'])
                    #trade_response = execute_trade_oanda(signal['action'], signal['price'])
                    return {
                        "data": data,
                        "signal": signal,
                        "trade": trade_response
                    }

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStreaming stopped.")
        return df

if __name__ == "__main__":
    strategy = ThresholdStrategy(buy_threshold=1.20, sell_threshold=1.28)
    df = stream_gbp_usd_data(strategy, interval=10)

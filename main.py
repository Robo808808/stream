from strategies.simple_threshold import ThresholdStrategy
from trading.oanda_executor import execute_trade_oanda
from trading.logger import log_trade
from marketdata.fetcher import get_fx_price, fetch_yf_fx
from config import LIVE_TRADING
import pandas as pd
import time
import datetime
from trading.sqlite_logger import init_db
init_db()

#def fetch_gbp_usd_data():
#    from random import uniform
#    return {"timestamp": datetime.datetime.now().isoformat(), "price": uniform(1.0, 1.4)}

def fetch_gbp_usd_data():
    """
    Attempts to use Alpha Vantage via get_fx_price(). If it fails,
    falls back to yfinance for local development.
    """
    data = get_fx_price()
    if data is None:
        print("⚠️  Alpha Vantage unavailable. Falling back to yfinance...")
        data = fetch_yf_fx()

    if not data:
        print("❌ No price data available from either source.")
        return None

    return data

def stream_gbp_usd_data(strategy, interval=10):
    df = pd.DataFrame(columns=["timestamp", "price"])

    try:
        while True:
            data = fetch_gbp_usd_data()
            if data:
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                signal = strategy.evaluate(df)

                print(f"[{data['timestamp']}] Price: {data['price']:.4f} → Signal: {signal['action']}")
                running_balance = 10000.00  # starting paper money in USD
                position = 0  # GBP units held

                if signal['action'] in ("BUY", "SELL"):
                    if LIVE_TRADING:
                        trade_response = execute_trade_oanda(signal['action'], signal['price'])
                    else:
                        trade_response = log_trade(signal['action'], signal['price'])

                    if signal['action'] == "BUY":
                        cost = signal['price'] * 1000
                        if running_balance >= cost:
                            running_balance -= cost
                            position += 1000
                    elif signal['action'] == "SELL" and position >= 1000:
                        running_balance += signal['price'] * 1000
                        position -= 1000

                    print(f"💰 Balance: ${running_balance:.2f}, Position: {position} GBP")
                    print(f"✅ Trade Response: {trade_response}")

            else:
                print("⏳ Waiting for valid data...")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🚦 Streaming stopped.")
        return df

if __name__ == "__main__":
    #strategy = ThresholdStrategy(buy_threshold=1.35, sell_threshold=1.38)
    #strategy = MovingAverageCrossoverStrategy(short_window=3, long_window=5)
    strategy = MovingAverageCrossoverStrategy(short_window=2, long_window=3)
    df = stream_gbp_usd_data(strategy, interval=10)
    print(f"📡 Live price: {data['price']:.5f}")
    print(f"🧠 Strategy in use: {strategy.__class__.__name__}")
    #print(f"📈 Signal: {signal['action']} ({signal.get('reason', 'no reason')})")
    print(f"[{data['timestamp']}] Price: {data['price']:.5f} → Signal: {signal['action']} ({signal.get('reason', '')})")

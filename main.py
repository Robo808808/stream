import yfinance as yf
import pandas as pd
import time


def fetch_gbp_usd_data():
    """
    Fetch GBP/USD exchange rate data from Yahoo Finance.
    Returns:
        dict: Latest price and timestamp.
    """
    ticker = "GBPUSD=X"  # Yahoo Finance ticker for GBP/USD
    data = yf.Ticker(ticker)
    hist = data.history(period="1d", interval="1m")  # Last 1 day, 1-minute interval

    # Get the most recent data point
    if not hist.empty:
        latest = hist.iloc[-1]
        return {
            "timestamp": latest.name,
            "price": latest["Close"]
        }
    else:
        return None


def stream_gbp_usd_data(interval=10):
    """
    Stream GBP/USD exchange rate data into a Pandas DataFrame.

    Args:
        interval (int): Time in seconds between data fetches.
    """
    df = pd.DataFrame(columns=["timestamp", "price"])

    try:
        while True:
            data = fetch_gbp_usd_data()
            if data:
                print(f"Fetched data: {data}")
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                print(df.tail(5))  # Display the last 5 rows

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStreaming stopped.")
        return df


# Start streaming
if __name__ == "__main__":
    df = stream_gbp_usd_data(interval=10)

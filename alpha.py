import requests
import pandas as pd
import time

# Alpha Vantage API details
API_KEY = "your_alpha_vantage_api_key"
BASE_URL = "https://www.alphavantage.co/query"


def fetch_fx_data():
    """
    Fetch the latest GBP/USD exchange rate using Alpha Vantage.
    Returns a dictionary with time and rate details.
    """
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "GBP",
        "to_currency": "USD",
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Extract relevant data
    rate_info = data.get("Realtime Currency Exchange Rate", {})
    return {
        "timestamp": rate_info.get("6. Last Refreshed"),
        "exchange_rate": float(rate_info.get("5. Exchange Rate", 0)),
    }


# Stream data into a Pandas DataFrame
def stream_fx_data(interval=10):
    """
    Continuously fetch FX data and append it to a Pandas DataFrame.

    Args:
        interval (int): Time in seconds between data fetches.
    """
    df = pd.DataFrame(columns=["timestamp", "exchange_rate"])

    try:
        while True:
            data = fetch_fx_data()
            print(f"Fetched data: {data}")

            # Append new data to the DataFrame
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

            # Display the DataFrame
            print(df)

            # Wait for the next interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStreaming stopped.")
        return df


# Start streaming
if __name__ == "__main__":
    df = stream_fx_data(interval=10)

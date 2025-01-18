import websocket
import json
import pandas as pd

# OANDA WebSocket URL
OANDA_WS_URL = "wss://stream-fxpractice.oanda.com/v3/accounts/your_account_id/pricing/stream"
ACCESS_TOKEN = "your_oanda_api_access_token"

def on_message(ws, message):
    """
    Callback to handle incoming WebSocket messages.
    """
    data = json.loads(message)
    if "bids" in data and "asks" in data:
        bid_price = float(data["bids"][0]["price"])
        ask_price = float(data["asks"][0]["price"])
        timestamp = data["time"]

        # Add data to a Pandas DataFrame
        row = {"timestamp": timestamp, "bid_price": bid_price, "ask_price": ask_price}
        df.loc[len(df)] = row
        print(df.tail(1))  # Display the latest row

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["timestamp", "bid_price", "ask_price"])

def stream_fx_data():
    """
    Stream FX data using OANDA's WebSocket API.
    """
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    ws = websocket.WebSocketApp(
        OANDA_WS_URL,
        header=headers,
        on_message=on_message,
    )
    ws.run_forever()

# Start streaming
if __name__ == "__main__":
    stream_fx_data()

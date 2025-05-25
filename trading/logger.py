import datetime
import json
from pathlib import Path

TRADE_LOG_FILE = Path("logs/trades.jsonl")
TRADE_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_trade(action: str, price: float, quantity: float = 1000, broker="mock"):
    trade = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "price": round(price, 5),
        "quantity": quantity,
        "broker": broker,
        "status": "mock"
    }
    with open(TRADE_LOG_FILE, "a") as f:
        f.write(json.dumps(trade) + "\n")
    print(f"📝 Mock trade logged: {trade}")
    return trade

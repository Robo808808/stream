import sqlite3
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def plot_daily_pnl():
    db_path = Path("logs/trades.db")
    if not db_path.exists():
        print("No trade data available.")
        return

    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM trades", conn, parse_dates=["timestamp"])
    conn.close()

    df["date"] = df["timestamp"].dt.date
    df["pnl"] = df.apply(lambda row: row["price"] * row["quantity"] if row["action"] == "SELL"
                         else -row["price"] * row["quantity"], axis=1)

    daily = df.groupby("date")["pnl"].sum().cumsum()
    daily.plot(title="Cumulative P&L", grid=True)
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.tight_layout()
    plt.savefig("logs/pnl.png")
    plt.show()

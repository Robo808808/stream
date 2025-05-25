import argparse
from strategies.moving_average import MovingAverageCrossoverStrategy
from main import stream_gbp_usd_data
import sqlite3
import csv
from pathlib import Path
from analytics.pnl import plot_daily_pnl


def export_trades_to_csv(output_file="trades.csv"):
    db_path = Path("logs/trades.db")
    if not db_path.exists():
        print("No trade history found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY timestamp")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"📤 Exported {len(rows)} trades to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream GBPUSD FX rates with strategy")
    parser.add_argument("--short", type=int, default=5)
    parser.add_argument("--long", type=int, default=20)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--export", help="Export trades to CSV", action="store_true")
    parser.add_argument("--pnl", help="Plot daily P&L chart", action="store_true")

    args = parser.parse_args()

    if args.export:
        export_trades_to_csv()
        exit(0)

    if args.pnl:
        plot_daily_pnl()
        exit(0)

    strategy = MovingAverageCrossoverStrategy(short_window=args.short, long_window=args.long)
    stream_gbp_usd_data(strategy, interval=args.interval)

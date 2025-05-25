import sqlite3
from pathlib import Path
import datetime

DB_PATH = Path("logs/trades.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            price REAL,
            quantity INTEGER,
            broker TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_trade_sqlite(action, price, quantity=1000, broker="mock"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO trades (timestamp, action, price, quantity, broker, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, action, round(price, 5), quantity, broker, "mock"))
    conn.commit()
    conn.close()

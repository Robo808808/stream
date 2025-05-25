from fastapi import APIRouter
import sqlite3
from pathlib import Path

router = APIRouter()

@router.get("/trades")
def get_trades(limit: int = 10):
    db_path = Path("logs/trades.db")
    if not db_path.exists():
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, action, price, quantity, broker, status
        FROM trades
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"timestamp": t, "action": a, "price": p, "qty": q, "broker": b, "status": s}
        for (t, a, p, q, b, s) in rows
    ]

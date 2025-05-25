from strategies.base import BaseStrategy
import pandas as pd

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.last_signal = "HOLD"

    def evaluate(self, df: pd.DataFrame) -> dict:
        if len(df) < self.long_window:
            return {"action": "HOLD", "reason": "insufficient data"}

        df['short_ma'] = df['price'].rolling(self.short_window).mean()
        df['long_ma'] = df['price'].rolling(self.long_window).mean()

        latest = df.iloc[-1]

        if latest['short_ma'] > latest['long_ma'] and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return {"action": "BUY", "price": latest['price']}
        elif latest['short_ma'] < latest['long_ma'] and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return {"action": "SELL", "price": latest['price']}
        else:
            return {"action": "HOLD", "price": latest['price']}

from strategies.base import BaseStrategy
import pandas as pd

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.last_signal = "HOLD"

    def evaluate(self, df):
        if len(df) < self.long_window:
            print(f"⏳ Waiting for enough data. Got {len(df)} rows, need {self.long_window}.")
            return {"action": "HOLD", "reason": "insufficient data"}

        df['short_ma'] = df['price'].rolling(self.short_window).mean()
        df['long_ma'] = df['price'].rolling(self.long_window).mean()

        short_ma = df['short_ma'].iloc[-1]
        long_ma = df['long_ma'].iloc[-1]
        latest_price = df['price'].iloc[-1]

        print(f"📉 MA Debug — Short MA({self.short_window}): {short_ma:.5f}, "
              f"Long MA({self.long_window}): {long_ma:.5f}, Price: {latest_price:.5f}")

        if short_ma > long_ma and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return {
                "action": "BUY",
                "price": latest_price,
                "reason": f"short MA {short_ma:.5f} > long MA {long_ma:.5f}"
            }

        elif short_ma < long_ma and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return {
                "action": "SELL",
                "price": latest_price,
                "reason": f"short MA {short_ma:.5f} < long MA {long_ma:.5f}"
            }

        else:
            return {
                "action": "HOLD",
                "price": latest_price,
                "reason": f"short MA {short_ma:.5f} ≈ long MA {long_ma:.5f}"
            }


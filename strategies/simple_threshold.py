from strategies.base import BaseStrategy

class ThresholdStrategy(BaseStrategy):
    def __init__(self, buy_threshold: float, sell_threshold: float):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def evaluate(self, df):
        if df.empty:
            return {"action": "HOLD", "reason": "no data"}

        latest_price = df.iloc[-1]["price"]

        print(f"📊 Threshold Debug — Price: {latest_price:.5f} | "
              f"Buy < {self.buy_threshold} | Sell > {self.sell_threshold}")

        if latest_price < self.buy_threshold:
            return {
                "action": "BUY",
                "price": latest_price,
                "reason": f"price {latest_price:.5f} < buy_threshold {self.buy_threshold}"
            }

        elif latest_price > self.sell_threshold:
            return {
                "action": "SELL",
                "price": latest_price,
                "reason": f"price {latest_price:.5f} > sell_threshold {self.sell_threshold}"
            }

        return {
            "action": "HOLD",
            "price": latest_price,
            "reason": f"price {latest_price:.5f} in threshold range"
        }

from strategies.base import BaseStrategy

class ThresholdStrategy(BaseStrategy):
    def __init__(self, buy_threshold: float, sell_threshold: float):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def evaluate(self, df):
        if df.empty:
            return {"action": "HOLD"}

        latest_price = df.iloc[-1]["price"]

        if latest_price < self.buy_threshold:
            return {"action": "BUY", "price": latest_price}
        elif latest_price > self.sell_threshold:
            return {"action": "SELL", "price": latest_price}
        else:
            return {"action": "HOLD", "price": latest_price}

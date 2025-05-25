from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def evaluate(self, df: 'pd.DataFrame') -> dict:
        """
        Evaluate the strategy on the given data.

        Returns:
            dict: A signal or order dict (e.g. {'action': 'BUY', 'confidence': 0.85})
        """
        print(f"📈 Latest price: {latest_price}, Buy < {self.buy_threshold}, Sell > {self.sell_threshold}")

        pass

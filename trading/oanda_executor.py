from trading.logger import log_trade
import oandapyV20
import oandapyV20.endpoints.orders as orders
from config import OANDA_ACCOUNT_ID, OANDA_TOKEN, OANDA_ENV
from config import disable_live_trading, LIVE_TRADING_ENABLED
from utils.retry import retry_with_backoff

client = oandapyV20.API(access_token=OANDA_TOKEN, environment=OANDA_ENV)

def execute_trade_oanda(action: str, price: float, units: int = 1000):
    side = "buy" if action == "BUY" else "sell"
    instrument = "GBP_USD"

    order_data = {
        "order": {
            "instrument": instrument,
            "units": str(units if side == "buy" else -units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }

    request = orders.OrderCreate(accountID=OANDA_ACCOUNT_ID, data=order_data)

    def send_request():
        # This is the function that will be retried
        client.request(request)
        return request.response

    try:
        return retry_with_backoff(send_request)
    except Exception as e:
        print(f"❌ OANDA trade failed after retries: {e}")
        disable_live_trading()
        print("⚠️ LIVE_TRADING disabled due to broker error.")
        return log_trade(action, price, units, broker="fallback-mock")


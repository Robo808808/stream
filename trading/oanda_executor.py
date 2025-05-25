import oandapyV20
import oandapyV20.endpoints.orders as orders

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
    client.request(request)
    return request.response

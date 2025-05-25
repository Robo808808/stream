from fastapi import FastAPI
import pandas as pd
from strategies.moving_average import MovingAverageCrossoverStrategy
from main import fetch_gbp_usd_data
from marketdata.fetcher import get_fx_price


app = FastAPI()
strategy = MovingAverageCrossoverStrategy()

@app.get("/fx/gbpusd")
def get_price_and_signal():
    #data = fetch_gbp_usd_data()
    data = get_fx_price()
    if data:
        signal = strategy.evaluate(pd.DataFrame([data]))
        return {"data": data, "signal": signal}
    return {"error": "No data"}

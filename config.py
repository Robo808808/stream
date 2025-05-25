import os

LIVE_TRADING = os.environ.get("LIVE_TRADING", "false").lower() == "true"
USE_REAL_MARKET_DATA = os.environ.get("USE_REAL_MARKET_DATA", "false").lower() == "true"
BROKER_NAME = os.environ.get("BROKER_NAME", "mock").lower()  # 'oanda', 'alpaca', 'mock'

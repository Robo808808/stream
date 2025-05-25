import os
from dotenv import load_dotenv

load_dotenv()

OANDA_TOKEN = os.getenv("OANDA_TOKEN")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
OANDA_ENV = os.getenv("OANDA_ENV", "practice")
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")

LIVE_TRADING = os.getenv("LIVE_TRADING", "false").lower() == "true"
USE_REAL_MARKET_DATA = os.getenv("USE_REAL_MARKET_DATA", "false").lower() == "true"
BROKER_NAME = os.getenv("BROKER_NAME", "mock")

USE_SIMULATED_PRICES = os.getenv("USE_SIMULATED_PRICES", "false").lower() == "true"

LIVE_TRADING_ENABLED = True  # Mutable flag

def disable_live_trading():
    global LIVE_TRADING_ENABLED
    LIVE_TRADING_ENABLED = False

from fastapi import APIRouter
from config import OANDA_ACCOUNT_ID, OANDA_TOKEN, OANDA_ENV
import oandapyV20
import oandapyV20.endpoints.accounts as accounts

router = APIRouter()

@router.get("/broker/status")
def check_oanda_status():
    try:
        client = oandapyV20.API(access_token=OANDA_TOKEN, environment=OANDA_ENV)
        r = accounts.AccountSummary(accountID=OANDA_ACCOUNT_ID)
        client.request(r)
        return {"status": "OK", "account": r.response}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

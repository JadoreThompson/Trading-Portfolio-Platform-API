import os
from dotenv import load_dotenv

# Pydantic
from pydantic_settings import BaseSettings

import oandapyV20
import oandapyV20.endpoints.accounts as accounts

load_dotenv()


class Settings(BaseSettings):
    OANDA_API_KEY: str = os.getenv("OANDA_API_KEY")
    OANDA_HEADER: dict = {"Authorization": f"Bearer {os.getenv("OANDA_API_KEY")}"}
    OANDA_BASE_URL: str = "https://api-fxpractice.oanda.com"
    OANDA_TRADING_ACCOUNT_ID: str = os.getenv("OANDA_TRADING_ACCOUNT_ID")
    OANDA_CLIENT: oandapyV20.API = oandapyV20.API(access_token=os.getenv("OANDA_API_KEY"))

# import json
settings = Settings()
# OANDA_CLIENT = oandapyV20.API(access_token=settings.OANDA_API_KEY)
# r = accounts.AccountSummary(settings.OANDA_TRADING_ACCOUNT_ID)
# OANDA_CLIENT.request(r)
# print(type(OANDA_CLIENT))
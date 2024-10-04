import os
from dotenv import load_dotenv

# Alpaca
import alpaca_trade_api
import alpaca_trade_api as trade_api
from alpaca.trading.client import TradingClient
from alpaca.trading.models import TradeAccount

# Pydantic
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    ALPACA_API_KEY: str = os.getenv('ALPACA_SANDBOX_API_KEY')
    ALPACA_SECRET_KEY: str = os.getenv('ALPACA_SANDBOX_SECRET_KEY')
    alpaca: alpaca_trade_api.rest.REST = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')
    trading_client: TradingClient = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    account: TradeAccount = trading_client.get_account()


settings = Settings()

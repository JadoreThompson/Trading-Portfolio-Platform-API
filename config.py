import os
from dotenv import load_dotenv
import alpaca_trade_api as trade_api


load_dotenv()

# Alpaca
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_API_KEY = os.getenv('ALPACA_SANDBOX_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SANDBOX_SECRET_KEY')
alpaca = trade_api.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')

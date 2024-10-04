import os
from dotenv import load_dotenv


load_dotenv()

# Alpaca
ALPACA_BASE_URL: str = "https://api.alpaca.markets/v1/assets"
ALPACA_API_KEY: str = os.getenv('ALPACA_SANDBOX_API_KEY')
ALPACA_SECRET_KEY: str = os.getenv('ALPACA_SANDBOX_SECRET_KEY')

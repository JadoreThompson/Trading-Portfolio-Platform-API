import aiohttp
import json

# Dir
import config


async def t():
    async with aiohttp.ClientSession() as session:
        async with session.get(config.ALPACA_BASE_URL + "/v1/assets") as rsp:
            data = await rsp.json()
            print(json.dumps(data, indent=4))


if __name__ == "__main__":
    # import asyncio
    # asyncio.run(t())
    from alpaca.trading.client import TradingClient
    tradingClient = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY)
    account = tradingClient.get_account()

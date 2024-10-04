import aiohttp
import json

# Dir
from config import ALPACA_BASE_URL


async def t():
    async with aiohttp.ClientSession() as session:
        async with session.get(ALPACA_BASE_URL + "/v1/assets") as rsp:
            data = await rsp.json()
            print(json.dumps(data, indent=4))


if __name__ == "__main__":
    import asyncio
    asyncio.run(t())

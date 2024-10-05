import json
from datetime import datetime
from typing import List, AsyncGenerator
import aiohttp

# DIR
from config import settings
from models import PnlFilterBody

# Oanda
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders

# FastAPI
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


# Functions
def get_pnl(params: dict) -> int | float:
    """
    :param params:
    :return: Sum of realised gains for that day
    """
    try:
        accountID = params['accountID']
        del params['accountID']

        r = orders.OrderList(accountID, params=params)
        settings.OANDA_CLIENT.request(r)
        data = r.response['orders']

        if params['day']:
            return sum([item['realizedPL'] for item in data if item['closeTime'] == params['day']])
        if params['start'] and params['end']:
            return sum([item['realizedPL'] for item in data if params['start'] <= item['closeTime'] <= params['end']])
        if params['start']:
            return sum([item['realizedPL'] for item in data if item['closeTime'] >= params['start']])
        if params['end']:
            return sum([item['realizedPL'] for item in data if item['closeTime'] >= params['end']])
    except Exception as e:
        print(type(e), str(e))


def get_risk_reward(params: dict) -> int | float:
    """
    :param params:
    :return: Average multiplier of the distance between the open price, stop price against the open price and take profit price
    """

    def risk_reward_calculation(trades: List) -> int | float:
        return sum([(float(trade['takeProfitOrder']['price']) - float(trade['price'])) /
                    (float(trade['price']) - float(trade['stopLossOrder']['price'])) for trade in trades]) / len(trades)

    try:
        accountID = params['accountID']
        del params['accountID']

        # Making Request
        r = orders.OrderList(accountID, params=params)
        settings.OANDA_CLIENT.request(r)
        data = r.response['orders']

        # Getting trades
        trades = []
        if params['day']:
            trades = [item for item in data if item['closeTime'] == params['day']]
        elif params['start'] and params['end']:
            trades = [item for item in data if params['start'] <= item['closeTime'] <= params['end']]
        elif params['start']:
            trades = [item for item in data if item['closeTime'] >= params['start']]
        elif params['end']:
            trades = [item for item in data if item['closeTime'] >= params['end']]

        if len(trades) > 0:
            return risk_reward_calculation(trades)
        else:
            return 0
    except Exception as e:
        print(type(e), str(e))


async def get_oanda_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    :return: Generator Object of a session with the Oanda Header
    """
    async with aiohttp.ClientSession(headers=settings.OANDA_HEADER) as session:
        yield session


# Initialisation
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/")
async def read_root():
    return {"message": "Running"}


@portfolio.get("/balance")
async def get_balance():
    try:
        r = accounts.AccountSummary(settings.OANDA_TRADING_ACCOUNT_ID)
        settings.OANDA_CLIENT.request(r)
        return JSONResponse(status_code=200, content={"balance": f"{float(r.response['account']['balance']): .2f}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})


@portfolio.post("/daily-pnl")
async def get_daily_pnl(body: PnlFilterBody):
    try:
        return JSONResponse(status_code=200, content={"pnl": get_pnl(body.dict())})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})


@portfolio.post("/orders")
async def get_trades(session: aiohttp.ClientSession = Depends(get_oanda_session)):
    async with session.get(f"{settings.OANDA_BASE_URL}/v3/accounts/{settings.OANDA_TRADING_ACCOUNT_ID}/orders") as rsp:
        data = await rsp.json()
    return data

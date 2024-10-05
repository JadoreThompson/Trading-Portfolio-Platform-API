import json
from datetime import datetime
from typing import List, AsyncGenerator
import aiohttp

# DIR
from config import settings
from models import MetricFilterObject, TradeObject

# Oanda
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.orders as orders


# FastAPI
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


# Functions
def pnl(params: dict) -> int | float:
    """
    :param params:
    :return: Sum of realised gains for that day
    """
    try:
        accountID = params['accountID']
        del params['accountID']

        # Making request
        r = orders.OrderList(accountID, params=params)
        settings.OANDA_CLIENT.request(r)
        data = r.response['orders']

        # Sorting
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


def risk_reward(params: dict) -> int | float:
    """
    :param params:
    :return: Average multiplier of the distance between the open price, stop price against the open price and take profit price
    """

    def risk_reward_calculation(trade_list: List) -> int | float:
        return sum([(float(trade['takeProfitOrder']['price']) - float(trade['price'])) /
                    (float(trade['price']) - float(trade['stopLossOrder']['price'])) for trade in trade_list]) / len(trade_list)

    try:
        accountID = params['accountID']
        del params['accountID']

        # Making Request
        r = trades.TradesList(accountID, params=params)
        settings.OANDA_CLIENT.request(r)
        data = r.response['orders']

        # Getting trades
        trade_list = []
        if params['day']:
            trade_list = [item for item in data if item['closeTime'] == params['day']]
        elif params['start'] and params['end']:
            trade_list = [item for item in data if params['start'] <= item['closeTime'] <= params['end']]
        elif params['start']:
            trade_list = [item for item in data if item['closeTime'] >= params['start']]
        elif params['end']:
            trade_list = [item for item in data if item['closeTime'] >= params['end']]

        if len(trade_list) > 0:
            return risk_reward_calculation(trade_list)
        else:
            return 0
    except Exception as e:
        print(type(e), str(e))


def sort_trades(trades_list: list, params: dict) -> List[dict]:
    """
    :param trades_list: List of trades to be sorted, where each trade is represented as a dictionary.
    :param params: Dictionary containing parameters for sorting trades, which may include criteria like date range or trade type.
    :return: List of Trade Objects, where each Trade Object contains the following fields:
        - price: (int | float) The opening price of the trade.
        - stop_loss: (int | float) The stop loss price set for the trade.
        - take_profit: (int | float) The take profit price set for the trade.
        - open_time: (datetime) The time when the trade was opened.
        - close_time: (Optional[datetime]) The time when the trade was closed (if applicable).
        - realised_pnl: (int | float) The realised profit or loss for the trade.
    """
    # Function implementation goes here

    try:
        new_trades_list = []
        if params['day']:
            new_trades_list = [item for item in trades_list if item['closeTime'] == params['day']]
        elif params['start'] and params['end']:
            new_trades_list = [item for item in trades_list if params['start'] <= item['closeTime'] <= params['end']]
        elif params['start']:
            new_trades_list = [item for item in trades_list if item['closeTime'] >= params['start']]
        elif params['end']:
            new_trades_list = [item for item in trades_list if item['closeTime'] >= params['end']]

        if len(new_trades_list) > 0:
            return [
                TradeObject(
                    price=item['price'],
                    stop_loss=float(item.get('stopLossOrder', {}).get('price', None)),
                    take_profit=float(item.get('takeProfitOrder', {}).get('price', None)),
                    open_time=str(item['openTime ']),
                    close_time=str(item.get('closeTime', None)),
                    realised_pnl=f"{float(item.get('realizedPL', None)): .2f}"
                ).dict()
                for item in new_trades_list
            ]
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


@portfolio.get("/balance", summary="Returns the balance for the account")
async def get_balance():
    try:
        r = accounts.AccountSummary(settings.OANDA_TRADING_ACCOUNT_ID)
        settings.OANDA_CLIENT.request(r)
        return JSONResponse(status_code=200, content={"balance": f"{float(r.response['account']['balance']): .2f}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})


@portfolio.post("/pnl", summary="Returns the pnl for the specified period of time")
async def get_pnl(body: MetricFilterObject):
    try:
        return JSONResponse(status_code=200, content={"pnl": pnl(body.dict())})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})


@portfolio.post("/risk-reward", summary="Returns the risk reward for the specified period of time")
async def get_risk_reward(body: MetricFilterObject):
    try:
        return JSONResponse(status_code=200, content={"risk_reward": risk_reward(body.dict())})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})


@portfolio.post("/trades", summary="Returns the trades opened in the specified period of time")
async def get_trades(body: MetricFilterObject):


    try:
        account_id = body.accountID
        del body.accountID
        print(json.dumps(body.dict(), indent=4))

        # Making request
        r = trades.TradesList(account_id, params={"params": body.dict()})
        settings.OANDA_CLIENT.request(r)
        return JSONResponse(status_code=200, content={"trades": sort_trades(r.response['trades'], body.dict())})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", "error": str(e)})

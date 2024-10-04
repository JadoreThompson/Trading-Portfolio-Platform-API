from alpaca.trading.requests import GetOrdersRequest

# DIR
from config import settings
from models import AccountBody, AllOrderBody

# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Initialisation
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/")
async def read_root():
    return {"message": "Connected to portfolio"}


@portfolio.post("/daily-pnl", summary="Returns todays equity change")
async def daily_pnl(account: AccountBody):
    try:
        equity = "{:.2f}".format(float(account.equity))
        return JSONResponse(status_code=200, content={"equity": equity})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), 'type': f"{type(e)}"})


@portfolio.post("/live-pnl")
async def live_pnl(account: AccountBody):
    """
    Utilises Websocket for live portfolio updates
    :param account:
    :return: Account Balance
    """
    pass


import json


@portfolio.post("/live-positions", summary="Returns all open positions")
async def get_live_positions(account: AccountBody):
    """
    :param account:
    :return: List of Live Positions
    """
    keys_to_remove = ["asset_marginable", "asset_id"]

    try:
        positions = settings.trading_client.get_all_positions()
        position_list = [{k: v for k, v in position.__dict__.items() if k not in keys_to_remove} for position in positions]
        return JSONResponse(status_code=200, content=position_list)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), 'type': f"{type(e)}"})


@portfolio.post("/all-orders", summary="Returns all orders for the account")
async def get_orders(all_order_request: AllOrderBody):
    try:
        del all_order_request.account_id
        params = GetOrdersRequest(**all_order_request.dict())
        orders = settings.trading_client.get_orders(filter=params)
        return JSONResponse(status_code=200, content=orders)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), 'type': f"{type(e)}"})


@portfolio.post("/sharpe-ratio ")

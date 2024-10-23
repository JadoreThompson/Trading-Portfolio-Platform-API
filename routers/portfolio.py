import json
from datetime import datetime
from typing import Annotated, List
from uuid import UUID

# SA
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Local
from config import API_KEY_ALIAS, ph
from dependencies import get_session, hash_api_key, get_session_2, get_user
from utils import get_trades
from db_models import Users, Orders

# FastAPI
from fastapi import APIRouter, Depends, Request, Header
from fastapi.responses import JSONResponse

from exceptions import DoesNotExist
from models import TradeRequestBody, Trade, AssetAllocationRequestBody

# Initialise
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/balance")
async def get_balance(user: Users = Depends(get_user)):
    try:
        return JSONResponse(status_code=200, content={'balance': user.balance})
    except DoesNotExist:
        raise
    except Exception as e:
        print(str(e))
        raise


@portfolio.post('/trades', response_model=List[Trade], summary="Returns a list of trades")
async def return_trades(body: TradeRequestBody, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(body, user)
        return [Trade(**item) for item in trades]
    except Exception as e:
        print(type(e), str(e))
        raise


@portfolio.post('/asset-allocation')
async def return_asset_allocation(body: AssetAllocationRequestBody, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(TradeRequestBody(**{key: value for key, value in body.dict().items()}), user)
        for item in trades:
            print(item['ticker'])

        # Counting occurrence of ticker
        ticker_occurrences = [
            (sum(1 for trade2 in trades if trade2.get('ticker', None) == ticker), ticker)
            for ticker in set(trade['ticker'] for trade in trades)
        ]

        # Calculating percentage
        amount_of_trades = len(trades)
        percentage = {
            item[1]: (item[0] / amount_of_trades) * 100
            for item in ticker_occurrences
        }
        return JSONResponse(status_code=200, content=percentage)
    except Exception:
        raise

import json
from datetime import datetime
from typing import Annotated, List
from uuid import UUID

# SA
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import API_KEY_ALIAS, ph

# Local
from dependencies import get_session, hash_api_key, get_session_2, get_user
from utils import get_trades
from db_models import Users, Orders

# FastAPI
from fastapi import APIRouter, Depends, Request, Header
from fastapi.responses import JSONResponse

from exceptions import DoesNotExist
from models import TradeRequestBody, Trade

# Initialise
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/balance")
async def get_balance(request: Request, user: Users = Depends(get_user), session: AsyncSession = Depends(get_session_2)):
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
        filtered_trades = [
            {
                key: (value if not isinstance(value, (datetime, UUID)) else str(value))
                for key, value in vars(trade).items()
                if value != None and key != '_sa_instance_state' and value != 'null'
             }
            for trade in trades
        ]
        return [Trade(**item) for item in filtered_trades]
    except Exception as e:
        print(type(e), str(e))
        raise

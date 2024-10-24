import json
import time
from datetime import datetime, timedelta
from typing import Annotated, List, Optional
from uuid import UUID
import asyncpg
from dateutil import parser

# SA
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
import sqlalchemy.exc

from arithemtic import sharpe, sortino
from config import REDIS_CLIENT
# Local
from dependencies import get_session, hash_api_key, get_session_2, get_user
from enums import Metrics
from utils import get_trades
from db_models import Users, Orders, Watchlist

# FastAPI
from fastapi import APIRouter, Depends, Request, Header, HTTPException
from fastapi.responses import JSONResponse

from exceptions import DoesNotExist
from models import TradeRequestBody, Trade, PeriodRequestBody, MetricRequestBody, \
    IsActiveRequestBody, AccountSummary, OrderID, WatchlistItem

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
async def return_trades(body: Optional[TradeRequestBody] = None, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, body)
        return [Trade(**item) for item in trades]
    except Exception as e:
        print(type(e), str(e))
        raise


@portfolio.post('/asset-allocation')
async def return_asset_allocation(body: IsActiveRequestBody, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, TradeRequestBody(**vars(body)))

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


@portfolio.post("/profits")
async def return_asset_allocation(body: PeriodRequestBody = None, user: Users = Depends(get_user)):
    """Returns the total unrealised and realised profit for the period of time"""
    try:
        trades = await get_trades(user, TradeRequestBody(**vars(body)) if body else None)
        return JSONResponse(status_code=200, content={
            'realised_pnl': sum(trade.get('realised_pnl', 0) for trade in trades)
        })
    except Exception:
        raise


@portfolio.post("/profits/daily")
async def return_daily_profits(api_key: str = Depends(hash_api_key), body: PeriodRequestBody = None, user: Users = Depends(get_user)):
    try:
        body = vars(body)
        cache_data = json.loads(REDIS_CLIENT.get(api_key).decode())
        result = [
            True for key in {body}
            if cache_data[key] == body[key]
        ]

        trades = await get_trades(user, TradeRequestBody(**body) if body else None)
        unique_dates = set(parser.parse(item['closed_at']).date() for item in trades)
        daily_profits = {
            str(date): sum(trade['realised_pnl']
            for trade in trades
            if parser.parse(trade['closed_at']).date() == date)
            for date in unique_dates
        }
        cache_data = {'daily_profits': daily_profits, 'created_at': datetime.now()}
        cache_data.update(body)
        REDIS_CLIENT.set(api_key, json.dumps(cache_data))
        return JSONResponse(status_code=200, content=daily_profits)
    except Exception:
        raise


@portfolio.post("/profits/monthly")
async def return_monthly_profits(body: PeriodRequestBody = None, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, TradeRequestBody(**vars(body)) if body else None)

        unique_dates = set(
            (parser.parse(item['closed_at']).year, parser.parse(item['closed_at']).month) for item in trades
        )
        monthly_profits = {
            str(date): 0
            for date in unique_dates
        }

        for trade in trades:
            closed_at = parser.parse(trade['closed_at'])
            date = (closed_at.year, closed_at.month)
            if date in unique_dates:
                monthly_profits[str(date)] += trade['realised_pnl']

        monthly_profits = {
            key.replace("(", "").replace(")", "").replace(", ", "-"): value
            for key, value in monthly_profits.items()
        }

        return JSONResponse(status_code=200, content=monthly_profits)
    except Exception:
        raise

@portfolio.post("/profits/yearly")
async def return_yearly_profits(body: PeriodRequestBody = None, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, TradeRequestBody(**vars(body)) if body else None)
        unique_dates = set(parser.parse(item['closed_at']).year for item in trades)
        yearly_profits = {
            str(date): 0
            for date in unique_dates
        }

        for trade in trades:
            year = parser.parse(trade['closed_at']).year
            yearly_profits[str(year)] += trade['realised_pnl']

        yearly_profits = {
            key.replace("(", "").replace(")", "").replace(", ", "-"): value
            for key, value in yearly_profits.items()
        }

        return JSONResponse(status_code=200, content=yearly_profits)
    except Exception:
        raise


@portfolio.post("/metrics")
async def return_metrics(body: MetricRequestBody, user: Users = Depends(get_user)):
    try:
        body = vars(body)
        trades = await get_trades(user, TradeRequestBody(**body) if body else None)

        metric = body.get('metric', None)
        if metric == Metrics.SHARPE.value:
            answer = sharpe([trade['realised_pnl'] for trade in trades])
        if metric == Metrics.SORTINO.value:
            answer = sortino([trade['realised_pnl'] for trade in trades])
        return JSONResponse(status_code=200, content={'metric': metric, 'value': answer})
    except UnboundLocalError:
        raise DoesNotExist('Metric')
    except DoesNotExist:
        raise
    except Exception:
        raise


@portfolio.post("/winrate")
async def return_winrate(body: IsActiveRequestBody, user: Users = Depends(get_user)):
    trades = await get_trades(user, TradeRequestBody(**vars(body)) if body else None)
    try:
        return JSONResponse(
            status_code=200,
            content={'winrate': (sum(1 for trade in trades if trade['realised_pnl'] > 0) / len(trades)) * 100}
        )
    except ZeroDivisionError:
        return JSONResponse(status_code=200, content={'winrate': 0.0})
    except Exception:
        raise


@portfolio.post("/volume")
async def return_volume(body: PeriodRequestBody, user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, TradeRequestBody(**vars(body)) if body else None)
        return JSONResponse(status_code=200, content={'total_volume': sum(trade['dollar_amount'] for trade in trades)})
    except Exception:
        raise


@portfolio.post("/summary", response_model=AccountSummary)
async def return_summary(user: Users = Depends(get_user)):
    try:
        trades = await get_trades(user, TradeRequestBody(**{'close_start': datetime.now().date() - timedelta(days=1)}))
        realised_pnl = sum(trade.get('realised_pnl', 0) for trade in trades)
        return AccountSummary(
            balance=user.balance,
            realised_pnl=realised_pnl,
            unrealised_pnl=sum(trade['unrealised_pnl'] for trade in trades),
        )
    except KeyError:
        raise DoesNotExist('Trades')
    except DoesNotExist:
        raise
    except Exception:
        raise


@portfolio.post("/trade", response_model=Trade)
async def return_order(body: OrderID, user: Users = Depends(get_user)):
    try:
        trade = await get_trades(user, None, body.order_id)
        return Trade(**trade)
    except sqlalchemy.exc.DBAPIError:
        raise DoesNotExist('Trade')
    except DoesNotExist:
        raise
    except Exception:
        raise


@portfolio.post("/watchlist", response_model=List[WatchlistItem])
async def return_watchlist(user: Users = Depends(get_user)):
    try:
        async with get_session() as session:
            result = await session.execute(select(Watchlist).where(Watchlist.user == user))
            return [WatchlistItem(ticker=vars(item).get('ticker', None)) for item in result.scalars().all()]
    except DoesNotExist:
        raise
    except Exception:
        raise


@portfolio.post("/watchlist/add")
async def add_to_watchlist(body: WatchlistItem, user: Users = Depends(get_user), session: AsyncSession = Depends(get_session_2)):
    try:
        result = await session.execute(insert(Watchlist).values(ticker=body.ticker, user_id=user.email))
        await session.commit()
        return HTTPException(status_code=200)
    except sqlalchemy.exc.IntegrityError:
        return JSONResponse(status_code=409, content={'error': f'{body.ticker} already in watchlist'})
    except DoesNotExist:
        raise
    except Exception:
        raise

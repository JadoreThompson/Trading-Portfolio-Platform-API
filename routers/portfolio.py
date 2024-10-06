from datetime import timedelta
from typing import List

# Oanda
import oandapyV20.endpoints.accounts as accounts

# Dir
from config import settings
from db_connection import get_conn
from models import TradeQueryParams, TradeObject, RiskRatioRequest, BalanceRequest
from tools import generate_select_args, sharpe_ratio, sortino_ratio, treynor_ratio, sharpe_std

# Fast API
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse


# Functions
async def retrieve_trades(conn, body) -> list:
    async with conn.transaction():
        cols, _, conditions, args = generate_select_args(body.dict())
        trades = await conn.fetch(f'''SELECT * FROM trades WHERE {conditions}''', *args)
    return trades


# Initialisation
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/")
async def read_root():
    return {"message": "Running"}


@portfolio.post("/balance")
async def get_balance(body: BalanceRequest):
    try:
        r = accounts.AccountDetails(body.account_id)
        settings.OANDA_CLIENT.request(r)
        return JSONResponse(status_code=200, content={'balance': r.response['balance']})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"{str(e)}"})


@portfolio.post("/trades", summary="Returns a list of all trades", response_model=List[TradeObject])
async def get_trades(body: TradeQueryParams, conn=Depends(get_conn)):
    trade_list = await retrieve_trades(conn, body)
    if not trade_list:
        raise HTTPException(status_code=500, detail='No trades found')
    return [TradeObject(**dict(trade)) for trade in trade_list]


# Important: Needs testing on a weekday when market open
@portfolio.post("/risk-adjusted-ratios", summary="Returns the sharpe, treynor and sortino ratios for period of time")
async def get_risk_ratios(body: RiskRatioRequest, conn=Depends(get_conn)):
    interval = body.interval

    # Getting trades
    del body.interval
    trades_list = await retrieve_trades(conn, body)

    # TODO: Make more efficient
    # Calculate ratios
    returns = []
    if interval == 'weekly':
        weeks = []

        while True:
            monday = body.start - timedelta(days=int(body.start.weekday()))
            sunday = monday + timedelta(days=6)

            if sunday >= body.end:
                sunday = body.end
                weeks.append((monday, sunday))
                break
            if monday >= body.end:
                break
            weeks.append((monday, sunday))

        for i in range(len(weeks)):
            weekly_returns = sum([trade['realised_pnl'] for trade in trades_list if weeks[i][0] >= trade['open_time'] <= weeks[i][1]])
            returns.append(weekly_returns)

    if interval == 'monthly':
        months = []

        while True:
            month_start = body.start - timedelta(days=int(body.start.day))
            month_end = month_start + timedelta(days=30)

            if month_end >= body.end:
                month_end = body.end
                months.append((month_start, month_end))
                break
            if month_start >= body.end:
                break
            months.append((month_start, month_end))

        for i in range(len(months)):
            monthly_returns = sum([trade['realised_pnl'] for trade in trades_list if months[i][0] >= trade['open_time'] <= months[i][1]])
            returns.append(monthly_returns)

    return sharpe_ratio(sum(returns), returns), sortino_ratio(sum(returns), returns), treynor_ratio(sum(returns), returns)


@portfolio.post("/max-drawdown", summary="Returns the lowest point in balance tracked for a specified period of time")
async def get_max_drawdown(body: TradeQueryParams, conn=Depends(get_conn)):
    trades = await retrieve_trades(conn, body)
    return JSONResponse(status_code=200, content={"max_drawdown": min(trade['closing_balance'] for trade in trades if trade['closing_balance'] < trade['starting_balance'])})


@portfolio.post("/std")
async def get_std(body: TradeQueryParams, conn=Depends(get_conn)):
    trades = await retrieve_trades(conn, body)
    return JSONResponse(status_code=200, content={"std": sharpe_std([item['realised_pnl'] for item in trades])})



# Dir
from db_connection import get_conn
from models import TradeRequest, TradeObject
from tools import generate_select_args

# Fast API
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Initialisation
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/")
async def read_root():
    return {"message": "Running"}


@portfolio.post("/trades", summary="Returns a list of all trades")
async def get_trades(body: TradeRequest, conn=Depends(get_conn)):
    try:
        async with conn.transaction():
            cols, _, conditions, args = generate_select_args(body.dict())
            trades = await conn.fetch(f'''SELECT * FROM trades WHERE {conditions}''', *args)
            return JSONResponse(status_code=200, content={"trades": [TradeObject(**dict(trade)).dict() for trade in trades]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"type": f"{type(e)}", 'error': f"{str(e)}"})

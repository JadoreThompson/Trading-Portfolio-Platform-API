# Dir
from db_connection import get_conn

# Fast API
from fastapi import APIRouter, Depends

# Initialisation
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/")
async def read_root():
    return {"message": "Running"}

@portfolio.post("/trades", summary="Returns a list of all trades")
async def get_trades(body: )
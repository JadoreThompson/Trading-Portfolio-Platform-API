from typing import Annotated

# SA
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Local
from dependencies import get_session, hash_api_key
from db_models import Users

# FastAPI
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

# Initialise
portfolio = APIRouter(prefix='/portfolio', tags=['portfolio'])


@portfolio.get("/balance")
async def get_balance(api_key: str = Depends(hash_api_key), session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Users).where(Users.api_key.in_([api_key])))
        key = result.scalars().first()
        return JSONResponse(status_code=200, content=vars(key))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), 'type': f"{type(e)}"})

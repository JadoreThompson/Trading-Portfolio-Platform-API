from contextlib import asynccontextmanager
from argon2 import PasswordHasher

# Local
from config import DB_ENGINE, API_KEY_ALIAS, ph

# FA
from fastapi import Request

# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession


# @asynccontextmanager
async def get_session():
    """
    Returns async SQLAlchemy session
    :return:
    """
    async with AsyncSession(DB_ENGINE) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def hash_api_key(request: Request) -> str:
    return str(ph.hash(request.headers.get(API_KEY_ALIAS)))

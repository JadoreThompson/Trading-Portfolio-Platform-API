from contextlib import asynccontextmanager
import argon2
from argon2 import PasswordHasher

# Local
from config import DB_ENGINE, API_KEY_ALIAS, ph
from db_models import Users

# FA
from fastapi import Request
from fastapi.responses import JSONResponse

# SQLAlchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import DoesNotExist


@asynccontextmanager
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


async def get_session_2():
    async with AsyncSession(DB_ENGINE) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def hash_api_key(request: Request) -> str:
    """Returns str of argon2 hashed api key"""
    return str(ph.hash(request.headers.get(API_KEY_ALIAS)))


async def get_user(request: Request) -> Users:
    """
    Uses the api key in header to indentify the user
    returns an object of type Users
    """
    async with get_session() as session:
        result = await session.execute(
            select(Users)
            .where(Users.api_key != None)
        )
        users = result.scalars().all()

        try:
            for user in users:
                try:
                    if ph.verify(user.api_key, request.headers.get(API_KEY_ALIAS)):
                        return user
                except argon2.exceptions.VerifyMismatchError:
                    continue
            raise DoesNotExist('User')
        except DoesNotExist:
            raise

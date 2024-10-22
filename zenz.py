import asyncio

import argon2
# SQLAlchemy
from sqlalchemy import select

# Local
from dependencies import get_session
from db_models import Users#, Orders


async def main():
    async with get_session() as sess:
        result = await sess.execute(select(Users).where(Users.email.in_(['sneakyredditpage@gmail.com'])))
        user = result.scalars().first()
        print(user)


if __name__ == "__main__":
    asyncio.run(main())

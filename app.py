from contextlib import asynccontextmanager
import asyncpg
from urllib.parse import quote
import os
from dotenv import load_dotenv

# Dir
import config
from routers.portfolio import portfolio

# FastAPI
from fastapi import FastAPI


load_dotenv()


# Functions
async def init_db_pool():
    return await asyncpg.create_pool(
        dsn=f"postgresql://{os.getenv("DB_USER")}:{quote(os.getenv("DB_PASSWORD"))}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}",
        min_size=1,
        max_size=10
    )


async def get_conn():
    async with app.state.db_pool.acquire() as conn:
        yield conn


# Functions
async def create_tables():
    """
    :return:
    - 4 Tables
        - Users
        - Accounts
        - Orders
        - Trades
    """

    async with app.state.db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id VARCHAR(255) PRIMARY KEY,
                user_id UUID REFERENCES users(user_id)
            );
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                account_id VARCHAR REFERENCES accounts(account_id),
                user_id UUID REFERENCES users(user_id),
                order_type VARCHAR(12) NOT NULL,
                symbol VARCHAR(20) NOT NULL,
                order_price DECIMAL NOT NULL,
                order_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                order_quantity DECIMAL NOT NULL,
                order_status VARCHAR(9) NOT NULL
            );
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                trade_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                order_id UUID REFERENCES orders(order_id),
                account_id VARCHAR REFERENCES accounts(account_id),
                symbol VARCHAR(20) NOT NULL,
                trade_open_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                trade_open_price DECIMAL NOT NULL,
                starting_balance DECIMAL NOT NULL,
                trade_close_time TIMESTAMP NULL,
                trade_close_price DECIMAL NULL,
                closing_balance DECIMAL NOT NULL,
                realised_pnl DECIMAL NULL DEFAULT 0.0,
                unrealised_pnl DECIMAL NULL DEFAULT 0.0,
                trade_status VARCHAR(16) NOT NULL
            );
        ''')


# Initialisation
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await init_db_pool()
    await create_tables()
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(portfolio)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)

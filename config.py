import os
from dotenv import load_dotenv
from urllib.parse import quote
from sqlalchemy.ext.asyncio import create_async_engine
from argon2 import PasswordHasher

load_dotenv()

# DB
DB_URI = \
    f"postgresql+asyncpg://{os.getenv("DB_USER")}:{quote(os.getenv('DB_PASSWORD'))}\
@{os.getenv("DB_HOST")}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
DB_ENGINE = create_async_engine(DB_URI)

API_KEY_ALIAS = 'api_key'

ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)

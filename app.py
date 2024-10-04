# Dir
import config

# FastAPI
from pydantic_settings import BaseSettings
from fastapi import FastAPI


class Settings(BaseSettings):
    ALPACA_BASE_URL: str = config.ALPACA_BASE_URL
    ALPACA_API_KEY: str = config.ALPACA_API_KEY
    ALPACA_SECRET_KEY: str = config.ALPACA_SECRET_KEY


app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)
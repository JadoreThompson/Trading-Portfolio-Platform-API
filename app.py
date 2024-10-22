# Local
from middleware import AuthenticateHeaderMiddleware, RateLimitingMiddleware

# FastAPI
from typing import Annotated
from fastapi import FastAPI, Header, Depends, Request, HTTPException


app = FastAPI()
app.add_middleware(AuthenticateHeaderMiddleware)
app.add_middleware(RateLimitingMiddleware)


@app.get('/')
async def read_root():
    return {"status": 'success', 'connected': True}


@app.get('/test')
async def test():
    return {'message': 'hi'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', port=80)

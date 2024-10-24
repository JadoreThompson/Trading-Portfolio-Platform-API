# Local
from uuid import uuid4

# SA
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from config import ph
from dependencies import get_session
from exceptions import DoesNotExist
from forms import LoginForm
from middleware import AuthenticateHeaderMiddleware, RateLimitingMiddleware
from db_models import Users
from routers.portfolio import portfolio

# FastAPI
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


origins = [
# All authorised endpoints
]

# Initialisation
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(AuthenticateHeaderMiddleware)
app.add_middleware(RateLimitingMiddleware)

app.include_router(portfolio)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


'''Exceptions'''
@app.exception_handler(Exception)
async def exception_handler(r: Request, e: Exception):
    return JSONResponse(status_code=500, content={"error": str(e), 'type': f"{type(e)}"})


@app.exception_handler(DoesNotExist)
async def does_not_exist_handler(request: Request, e: DoesNotExist):
    return JSONResponse(status_code=404, content={"message": e.message})


'''Endpoints'''
@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html'
    )


@app.get('/login')
async def get_login():
    web_app_login_url = "login"
    return RedirectResponse(web_app_login_url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', port=80)

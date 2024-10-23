from datetime import timedelta, datetime
from argon2 import PasswordHasher

# Local
from db_models import Users
from dependencies import get_session
from config import API_KEY_ALIAS, ph

# Starlette
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# SQLAlchemy
from sqlalchemy import select


EXCLUDED_PATHS = [
    '/', '/login', '/login-user', '/register', '/generate-key'
]


class AuthenticateHeaderMiddleware(BaseHTTPMiddleware):
    _KEYS = ['dog']

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        api_key = request.headers.get(API_KEY_ALIAS, None)

        if not api_key:
            return JSONResponse(status_code=401, content={'Error': 'API Key not provided'})

        async with get_session() as sess:
            result = await sess.execute(select(Users).where(Users.api_key == str(ph.hash(api_key))))
            if not result.scalars().first():
                return JSONResponse(status_code=401, content={'Error': 'API Key Invalid'})

        response = await call_next(request)
        return response


class RateLimitingMiddleware(BaseHTTPMiddleware):
    _TIME_LIMIT = timedelta(minutes=1)
    _REQUEST_LIMIT = 5

    def __init__(self, app):
        super().__init__(app)
        self.request_counter = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        api_key = request.headers.get(API_KEY_ALIAS)

        self.request_counter.setdefault(api_key, [0, datetime.now()])
        api_key_usage = self.request_counter.get(api_key)

        if (datetime.now() - api_key_usage[1]) < self._TIME_LIMIT and api_key_usage[0] >= self._REQUEST_LIMIT:
            return JSONResponse(status_code=401, content={'Error': 'Rate Limit reached'})

        if (datetime.now() - api_key_usage[1]) >= self._TIME_LIMIT and api_key_usage[0] >= self._REQUEST_LIMIT:
            self.request_counter[api_key] = [0, datetime.now()]

        if (datetime.now() - api_key_usage[1]) < self._TIME_LIMIT and api_key_usage[0] != 5:
            self.request_counter[api_key][0] += 1

        response = await call_next(request)
        return response

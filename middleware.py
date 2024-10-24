from contextlib import asynccontextmanager
from datetime import timedelta, datetime

import argon2.exceptions
from argon2 import PasswordHasher

# Local
from db_models import Users
from dependencies import get_session
from config import API_KEY_ALIAS, ph
from exceptions import DoesNotExist

# Starlette
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# SQLAlchemy
from sqlalchemy import select


_EXCLUDED_PATHS = [
    '/portfolio'
]

class AuthenticateHeaderMiddleware(BaseHTTPMiddleware):
    """
    Checks that the api key is present in header and that it matches
    with an existing key stored
    """
    _KEYS = [
        "$argon2id$v=19$m=102400,t=2,p=8$1F7sQVRlqtD0lYmWTEsKcA$e2q5x2hbsBo2cxfIWXfco9bXq5A45dXL8dA3HP/UbAE",
        'dog'
    ]



    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        - Passes through EXCLUDED_PATHS
        - Checks with DB if the key's hash is present
        """
        # TODO: Store the api key in session to reduce load
        if not any(request.url.path.startswith(path) for path in _EXCLUDED_PATHS):
            response = await call_next(request)
            return response

        api_key = request.headers.get(API_KEY_ALIAS, None)
        if not api_key:
            return JSONResponse(status_code=401, content={'error': 'API Key not provided'})

        async with get_session() as session:
            result = await session.execute(
                select(Users)
                .where(Users.api_key != None)
            )

            users = result.scalars().all()
            if not users:
                return JSONResponse(status_code=401, content={'error': 'Something went wrong'})
            for user in users:
                try:
                    if ph.verify(user.api_key, api_key):
                        return await call_next(request)
                except argon2.exceptions.VerifyMismatchError:
                    continue
            return JSONResponse(status_code=401, content={'Invalid key'})





class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Keeps track of the user's request
    stores the request count and request date in a list
    [count, date]
    """
    _TIME_LIMIT = timedelta(minutes=1)
    _REQUEST_LIMIT = 5

    def __init__(self, app):
        super().__init__(app)
        self.request_counter = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not any(request.url.path.startswith(path) for path in _EXCLUDED_PATHS):
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

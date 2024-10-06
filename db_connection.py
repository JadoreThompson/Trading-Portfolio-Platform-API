from fastapi import Request


async def get_conn(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        try:
            yield conn
        finally:
            await request.app.state.db_pool.release(conn)

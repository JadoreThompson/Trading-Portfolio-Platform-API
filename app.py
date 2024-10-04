# Dir
import config
from routers.portfolio import portfolio

# FastAPI
from fastapi import FastAPI


# Initialisation
app = FastAPI()
app.include_router(portfolio)


@app.get('/')
async def read_root():
    return {"message": "Running"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)
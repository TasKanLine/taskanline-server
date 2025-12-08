import asyncio
import uvicorn
from fastapi import FastAPI

from core.config import settings
from models import setup_database
from api import router as api_router

HOST = settings.core.HOST
PORT = settings.core.PORT


app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    asyncio.run(setup_database())
    uvicorn.run(app, host=HOST, port=PORT)

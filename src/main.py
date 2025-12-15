import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from models import setup_database
from api import router as api_router

HOST = settings.core.HOST
PORT = settings.core.PORT
ALLOWED_ORIGINS = settings.core.ALLOWED_ORIGINS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    asyncio.run(setup_database())
    uvicorn.run(app, host=HOST, port=PORT, reload=True)

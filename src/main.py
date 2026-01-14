import uvicorn
from contextlib import asynccontextmanager  # Импортируем
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from models import setup_database
from api import router as api_router

HOST = settings.core.HOST
PORT = settings.core.PORT
ALLOWED_ORIGINS = settings.core.ALLOWED_ORIGINS


# === ВНЕДРЯЕМ LIFESPAN ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Логика при старте приложения (внутри правильного Loop)
    await setup_database()
    yield
    # Логика при остановке (например, закрытие пула, если нужно)
    # from database.session import engine
    # await engine.dispose()


app = FastAPI(lifespan=lifespan)  # Подключаем lifespan

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Убираем asyncio.run(setup_database())
    # Запускаем uvicorn, он сам вызовет lifespan при старте
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    # reload=True полезен для разработки, но в Docker лучше без него или с контролем

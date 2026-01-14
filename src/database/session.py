from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

if settings.db.HOST:
    DATABASE = settings.db.url()
else:
    DATABASE = settings.db_test.url()

# Рекомендация: добавь pool_pre_ping=True, чтобы рвать протухшие соединения
engine = create_async_engine(
    DATABASE,
    echo=False,  # Можно True для отладки SQL запросов
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with SessionLocal() as session:
        yield session

from database.session import engine, Base
from models.users import Base


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

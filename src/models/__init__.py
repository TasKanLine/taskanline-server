from core.database import engine
from models.users import Base
from models.users import User, UserProfile
from models.tasks import Project, Board, Column, Task


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

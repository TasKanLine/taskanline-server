from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.auth import UserCreate

async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(email=user_data.email, hashed_password=user_data.password, username=user_data.username)
    session.add(user)
    await session.commit()
    return user

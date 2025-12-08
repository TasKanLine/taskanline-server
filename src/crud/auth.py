from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.users import User
from schemas.auth import UserCreate

ph = PasswordHasher()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        password=ph.hash(user_data.password),
        username=user_data.username,
    )
    session.add(user)
    await session.commit()
    return user


async def get_user_by_email_and_password(
    session: AsyncSession, email: str, password: str
) -> User | None:
    user = await session.scalar(select(User).where(User.email == email))
    if user:
        try:
            ph.verify(user.password, password)
            return user
        except VerifyMismatchError:
            return None
    return None


async def user_exists(session: AsyncSession, email: str, username: str) -> bool:
    return (
        await session.scalar(
            select(User)
            .where(User.email == email)
            .union_all(select(User).where(User.username == username))
        )
        is not None
    )


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    return await session.scalar(select(User).where(User.email == email))


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return await session.scalar(select(User).where(User.username == username))

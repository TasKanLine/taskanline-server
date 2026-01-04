from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from models.users import User, UserProfile
from schemas.auth import UserCreate, UserResponse

ph = PasswordHasher()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        password=ph.hash(user_data.password),
        username=user_data.username,
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    user_profile = UserProfile(
        user_id=user.id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    session.add(user_profile)
    await session.flush()
    await session.refresh(user_profile)
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


async def get_user_by_username_or_email(
    session: AsyncSession, username_or_email: str
) -> User | None:
    return await session.scalar(
        select(User)
        .where(User.username == username_or_email)
        .union_all(select(User).where(User.email == username_or_email))
    )


async def get_user_profile_by_username(
    session: AsyncSession, username: str
) -> UserResponse | None:
    user = await get_user_by_username(session, username)
    if user:
        user_profile = await session.get(UserProfile, user.id)
        return UserResponse(
            email=user.email,
            username=user.username,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            birth_date=user_profile.birth_date,
            phone_number=user_profile.phone_number,
            avatar_url=user_profile.avatar,
        )
    return None


async def get_user_profile_by_username_or_email(
    session: AsyncSession, username_or_email: str
) -> UserProfile | None:
    user = await get_user_by_username_or_email(session, username_or_email)
    if user:
        return await session.get(UserProfile, user.id)
    return None

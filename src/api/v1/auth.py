from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from core.depends import AsyncSessionDep
from crud import auth as crud
from schemas import auth as schemas


router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=schemas.UserResponse)
async def signup(session: AsyncSessionDep, user: schemas.UserCreate):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    try:
        await crud.create_user(session, user)
        return schemas.UserResponse(
            status="User created successfully", email=user.email, username=user.username
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.post("/login", response_model=schemas.UserModel)
async def login(session: AsyncSessionDep, user_data: schemas.UserLogin):
    if not user_data.email:
        raise HTTPException(status_code=400, detail="Email or username is required")
    if not user_data.password:
        raise HTTPException(status_code=400, detail="Password is required")
    try:
        user = await crud.get_user_by_email_and_password(
            session, user_data.email, user_data.password
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.UserModel(id=user.id, email=user.email, username=user.username)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")

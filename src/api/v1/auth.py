from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from crud import auth as crud
from schemas import auth as schemas
from database.session import get_session


router = APIRouter(prefix="/auth")

SessionDep = Annotated[AsyncSession, Depends(get_session)]

@router.post("/signup", response_model=schemas.UserResponse)
async def signup(session: SessionDep, user: schemas.UserCreate):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    try:
        await crud.create_user(session, user)
        return schemas.UserResponse(status="User created successfully", email=user.email, username=user.username)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")

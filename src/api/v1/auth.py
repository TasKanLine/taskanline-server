from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.exc import IntegrityError

from core.depends import AsyncSessionDep, SecurityDep, get_current_user
from core.security import security
from crud import auth as crud
from schemas import auth as schemas
from models import users


router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=schemas.UserResponse)
async def signup(session: AsyncSessionDep, user: schemas.UserCreate):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not user.first_name:
        raise HTTPException(status_code=400, detail="First name is required")
    if not user.last_name:
        raise HTTPException(status_code=400, detail="Last name is required")
    try:
        await crud.create_user(session, user)
        return schemas.UserResponse(
            status="User created successfully", email=user.email, username=user.username, first_name=user.first_name, last_name=user.last_name
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.post("/login", response_model=schemas.UserModel)
async def login(
    session: AsyncSessionDep, user_data: schemas.UserLogin, response: Response
):
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
        token = security.create_access_token(
            uid=str(user.id), dict={"email": user.email, "username": user.username}
        )
        response.set_cookie(key="access_token", value=token)
        return schemas.UserModel(id=user.id, email=user.email, username=user.username)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.get("/protected")
async def protected(user: str = Depends(get_current_user)):
    return {"message": "You are authorized"}

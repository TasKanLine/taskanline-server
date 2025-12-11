from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.exc import IntegrityError
from authx import AuthX, AuthXConfig

from core.depends import AsyncSessionDep
from crud import auth as crud
from schemas import auth as schemas


router = APIRouter(prefix="/auth")

config= AuthXConfig()
config.JWT_SECRET_KEY = "your_secret_key"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_REFRESH_COOKIE_NAME = "refresh_token"
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies"]

authx = AuthX(config)

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
async def login(session: AsyncSessionDep, user_data: schemas.UserLogin, response: Response):
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
        token = authx.create_access_token(uid=str(user.id), dict={"email": user.email, "username": user.username})
        response.set_cookie(key="access_token", value=token)
        print(token)
        return schemas.UserModel(id=user.id, email=user.email, username=user.username)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")

@router.get("/protected", dependencies=[Depends(authx.access_token_required)])
async def protected():
    return {"message": "You are authorized"}

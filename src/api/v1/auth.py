import logging

from fastapi import APIRouter, HTTPException, Response, Request
from sqlalchemy.exc import IntegrityError

from core.depends import AsyncSessionDep, SecurityDep
from core.security import security
from crud import auth as crud
from schemas import auth as schemas
from models import users


logging.basicConfig(level=logging.NOTSET)
# log = logging.getLogger(name=__name__)
router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=schemas.UserResponse)
async def signup(session: AsyncSessionDep, user: schemas.UserCreate, r: Request):
    print(r.url)
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
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            birth_date=None,
            phone_number=None,
            avatar_url=None,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.post("/login", response_model=schemas.UserModel)
async def login(
    session: AsyncSessionDep, user_data: schemas.UserLogin, response: Response, r: Request
):
    logging.info(r.url)
    print(r.url)
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
            uid=str(user.username),
            dict={"email": user.email, "username": user.username},
        )
        response.set_cookie(key="access_token", value=token, samesite="none", secure=True)
        return schemas.UserModel(id=user.id, email=user.email, username=user.username)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.get("/me")
async def protected(user: SecurityDep, session: AsyncSessionDep, response: Response):
    try:
        username = user.sub  # pyright: ignore[reportAttributeAccessIssue]
        user_data = await crud.get_user_profile_by_username(session, username)
    except TypeError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "You are authorized", "user_data": user_data}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

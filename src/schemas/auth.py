import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    password: str = Field(..., min_length=8, description="User's password")


class UserLoginEmail(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")


class UserLoginUsername(BaseModel):
    username: str = Field(..., description="User's username")
    password: str = Field(..., min_length=8, description="User's password")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")


class UserResponse(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    birth_date: datetime.date | None = Field(..., description="User's birth date")
    phone_number: str | None = Field(..., description="User's phone number")
    avatar_url: str | None = Field(..., description="User's avatar URL")


class UserModel(BaseModel):
    id: int = Field(..., description="User's ID")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")

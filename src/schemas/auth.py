from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")
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
    status: str = Field(..., description="Response message")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")


class UserModel(BaseModel):
    id: int = Field(..., description="User's ID")
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., description="User's username")

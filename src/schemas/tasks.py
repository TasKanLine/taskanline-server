from datetime import datetime, date

from pydantic import BaseModel, Field


# --- Project ---

class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Board ---

class BoardCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class BoardResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Column ---

class ColumnCreate(BaseModel):
    name: str = Field(..., max_length=50)
    position: int


class ColumnResponse(BaseModel):
    id: int
    board_id: int
    name: str
    position: int

    model_config = {"from_attributes": True}


# --- Task ---

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    priority: str = Field("medium", pattern="^(low|medium|high|critical)$")
    assignee_id: int | None = None
    due_date: date | None = None
    position: int


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    priority: str | None = Field(None, pattern="^(low|medium|high|critical)$")
    assignee_id: int | None = None
    due_date: date | None = None
    position: int | None = None


class TaskResponse(BaseModel):
    id: int
    column_id: int
    creator_id: int
    assignee_id: int | None
    title: str
    description: str | None
    priority: str
    due_date: date | None
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskMove(BaseModel):
    column_id: int
    position: int

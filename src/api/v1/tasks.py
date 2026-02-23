from fastapi import APIRouter, HTTPException

from core.depends import AsyncSessionDep, SecurityDep
from crud import auth as auth_crud
from crud import tasks as crud
from models.tasks import Column as ColumnModel
from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse, TaskMove

router = APIRouter(tags=["tasks"])


async def _get_current_user_id(session: AsyncSessionDep, user: SecurityDep) -> int:
    username = user.sub  # pyright: ignore[reportAttributeAccessIssue]
    db_user = await auth_crud.get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_user.id


@router.post("/columns/{column_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    column_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
    data: TaskCreate,
):
    creator_id = await _get_current_user_id(session, user)
    col = await session.get(ColumnModel, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    async with session.begin():
        task = await crud.create_task(session, column_id, creator_id, data)
    return task


@router.get("/columns/{column_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    column_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    col = await session.get(ColumnModel, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return await crud.get_tasks_by_column(session, column_id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
    data: TaskUpdate,
):
    await _get_current_user_id(session, user)
    async with session.begin():
        task = await crud.update_task(session, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}/move", response_model=TaskResponse)
async def move_task(
    task_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
    data: TaskMove,
):
    await _get_current_user_id(session, user)
    col = await session.get(ColumnModel, data.column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    async with session.begin():
        task = await crud.move_task(session, task_id, data.column_id, data.position)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    async with session.begin():
        await crud.delete_task(session, task_id)

from fastapi import APIRouter, HTTPException

from core.depends import AsyncSessionDep, SecurityDep
from crud import auth as auth_crud
from crud import tasks as crud
from models.tasks import Column as ColumnModel
from schemas.tasks import ColumnCreate, ColumnResponse

router = APIRouter(tags=["columns"])


async def _get_current_user_id(session: AsyncSessionDep, user: SecurityDep) -> int:
    username = user.sub  # pyright: ignore[reportAttributeAccessIssue]
    db_user = await auth_crud.get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_user.id


@router.post("/boards/{board_id}/columns", response_model=ColumnResponse, status_code=201)
async def create_column(
    board_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
    data: ColumnCreate,
):
    await _get_current_user_id(session, user)
    board = await crud.get_board(session, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    async with session.begin():
        column = await crud.create_column(session, board_id, data)
    return column


@router.get("/boards/{board_id}/columns", response_model=list[ColumnResponse])
async def list_columns(
    board_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    board = await crud.get_board(session, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return await crud.get_columns_by_board(session, board_id)


@router.delete("/columns/{column_id}", status_code=204)
async def delete_column(
    column_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    col = await session.get(ColumnModel, column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    async with session.begin():
        await crud.delete_column(session, column_id)

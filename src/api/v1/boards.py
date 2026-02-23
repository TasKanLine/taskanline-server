from fastapi import APIRouter, HTTPException

from core.depends import AsyncSessionDep, SecurityDep
from crud import auth as auth_crud
from crud import tasks as crud
from schemas.tasks import BoardCreate, BoardResponse

router = APIRouter(tags=["boards"])


async def _get_current_user_id(session: AsyncSessionDep, user: SecurityDep) -> int:
    username = user.sub  # pyright: ignore[reportAttributeAccessIssue]
    db_user = await auth_crud.get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_user.id


@router.post("/projects/{project_id}/boards", response_model=BoardResponse, status_code=201)
async def create_board(
    project_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
    data: BoardCreate,
):
    owner_id = await _get_current_user_id(session, user)
    project = await crud.get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    async with session.begin():
        board = await crud.create_board(session, project_id, data)
    return board


@router.get("/projects/{project_id}/boards", response_model=list[BoardResponse])
async def list_boards(
    project_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    owner_id = await _get_current_user_id(session, user)
    project = await crud.get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.get_boards_by_project(session, project_id)


@router.get("/boards/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    await _get_current_user_id(session, user)
    board = await crud.get_board(session, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.delete("/boards/{board_id}", status_code=204)
async def delete_board(
    board_id: int,
    session: AsyncSessionDep,
    user: SecurityDep,
):
    owner_id = await _get_current_user_id(session, user)
    board = await crud.get_board(session, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    project = await crud.get_project(session, board.project_id)
    if not project or project.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    async with session.begin():
        await crud.delete_board(session, board_id)

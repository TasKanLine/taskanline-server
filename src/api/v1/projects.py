from fastapi import APIRouter, HTTPException

from core.depends import AsyncSessionDep, SecurityDep
from crud import auth as auth_crud
from crud import tasks as crud
from schemas.tasks import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


async def _get_current_user_id(session: AsyncSessionDep, user: SecurityDep) -> int:
    username = user.sub  # pyright: ignore[reportAttributeAccessIssue]
    db_user = await auth_crud.get_user_by_username(session, username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_user.id


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    session: AsyncSessionDep,
    user: SecurityDep,
    data: ProjectCreate,
):
    owner_id = await _get_current_user_id(session, user)
    async with session.begin():
        project = await crud.create_project(session, owner_id, data)
    return project


@router.get("", response_model=list[ProjectResponse])
async def list_projects(session: AsyncSessionDep, user: SecurityDep):
    owner_id = await _get_current_user_id(session, user)
    return await crud.get_projects_by_owner(session, owner_id)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
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
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
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
    async with session.begin():
        await crud.delete_project(session, project_id)

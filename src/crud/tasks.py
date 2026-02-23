from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.tasks import Project, Board, Column, Task
from schemas.tasks import (
    ProjectCreate,
    BoardCreate,
    ColumnCreate,
    TaskCreate,
    TaskUpdate,
)


# --- Projects ---

async def create_project(
    session: AsyncSession, owner_id: int, data: ProjectCreate
) -> Project:
    project = Project(owner_id=owner_id, name=data.name, description=data.description)
    session.add(project)
    await session.flush()
    return project


async def get_project(session: AsyncSession, project_id: int) -> Project | None:
    return await session.get(Project, project_id)


async def get_projects_by_owner(
    session: AsyncSession, owner_id: int
) -> list[Project]:
    result = await session.scalars(
        select(Project)
        .where(Project.owner_id == owner_id)
        .order_by(Project.created_at.desc())
    )
    return list(result.all())


async def delete_project(session: AsyncSession, project_id: int) -> None:
    project = await session.get(Project, project_id)
    if project:
        await session.delete(project)


# --- Boards ---

async def create_board(
    session: AsyncSession, project_id: int, data: BoardCreate
) -> Board:
    board = Board(project_id=project_id, name=data.name, description=data.description)
    session.add(board)
    await session.flush()
    return board


async def get_board(session: AsyncSession, board_id: int) -> Board | None:
    return await session.get(Board, board_id)


async def get_boards_by_project(
    session: AsyncSession, project_id: int
) -> list[Board]:
    result = await session.scalars(
        select(Board)
        .where(Board.project_id == project_id)
        .order_by(Board.created_at.asc())
    )
    return list(result.all())


async def delete_board(session: AsyncSession, board_id: int) -> None:
    board = await session.get(Board, board_id)
    if board:
        await session.delete(board)


# --- Columns ---

async def create_column(
    session: AsyncSession, board_id: int, data: ColumnCreate
) -> Column:
    column = Column(board_id=board_id, name=data.name, position=data.position)
    session.add(column)
    await session.flush()
    return column


async def get_columns_by_board(
    session: AsyncSession, board_id: int
) -> list[Column]:
    result = await session.scalars(
        select(Column)
        .where(Column.board_id == board_id)
        .order_by(Column.position.asc())
    )
    return list(result.all())


async def delete_column(session: AsyncSession, column_id: int) -> None:
    column = await session.get(Column, column_id)
    if column:
        await session.delete(column)


# --- Tasks ---

async def create_task(
    session: AsyncSession, column_id: int, creator_id: int, data: TaskCreate
) -> Task:
    task = Task(
        column_id=column_id,
        creator_id=creator_id,
        assignee_id=data.assignee_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        due_date=data.due_date,
        position=data.position,
    )
    session.add(task)
    await session.flush()
    return task


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return await session.get(Task, task_id)


async def get_tasks_by_column(
    session: AsyncSession, column_id: int
) -> list[Task]:
    result = await session.scalars(
        select(Task)
        .where(Task.column_id == column_id)
        .order_by(Task.position.asc())
    )
    return list(result.all())


async def update_task(
    session: AsyncSession, task_id: int, data: TaskUpdate
) -> Task | None:
    task = await session.get(Task, task_id)
    if not task:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    await session.flush()
    return task


async def move_task(
    session: AsyncSession, task_id: int, column_id: int, position: int
) -> Task | None:
    task = await session.get(Task, task_id)
    if not task:
        return None
    task.column_id = column_id
    task.position = position
    await session.flush()
    return task


async def delete_task(session: AsyncSession, task_id: int) -> None:
    task = await session.get(Task, task_id)
    if task:
        await session.delete(task)

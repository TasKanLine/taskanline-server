from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.projects import router as projects_router
from api.v1.boards import router as boards_router
from api.v1.columns import router as columns_router
from api.v1.tasks import router as tasks_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(projects_router)
router.include_router(boards_router)
router.include_router(columns_router)
router.include_router(tasks_router)

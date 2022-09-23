from fastapi import APIRouter
from .tasks import task_router
from .users import user_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(task_router)
api_router.include_router(user_router)

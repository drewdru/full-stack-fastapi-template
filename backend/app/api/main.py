from fastapi import APIRouter

from app.api.routes import private, users, utils
from app.core.config import settings
from app.api.routes import login
from app.api.routes.items import items_controller

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items_controller.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

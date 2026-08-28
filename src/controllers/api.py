from fastapi import APIRouter
from src.controllers.user_controller import router as user_router

api_router = APIRouter(prefix="/api/v1")


# Include all entity routers here
api_router.include_router(user_router)

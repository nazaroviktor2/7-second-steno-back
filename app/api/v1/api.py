from fastapi import APIRouter

from app.api.v1.endpoints import file, auth

api_router = APIRouter()
api_router.include_router(file.router, prefix="/v1/file", tags=["File"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])

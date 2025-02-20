from fastapi import APIRouter

from app.api.routes import generate_image

api_router = APIRouter()
api_router.include_router(generate_image.router)

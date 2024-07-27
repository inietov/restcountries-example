from fastapi import APIRouter

from app.api.routes import countries, dadjokes

api_router = APIRouter()

api_router.include_router(countries.router, prefix="/api",tags=["api"])
api_router.include_router(dadjokes.router, prefix="", tags=["dad_jokes"])
from fastapi import APIRouter

from app.api.routes import countries

api_router = APIRouter()
api_router.include_router(countries.router, tags=["api"])
import httpx
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.api.main import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient(timeout=10.0)
    yield
    await app.requests_client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
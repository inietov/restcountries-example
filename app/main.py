import httpx
import sqlite3
import json
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

app = FastAPI(lifespan=lifespan)


@app.get("/countries")
async def get_countries(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get("https://restcountries.com/v3.1/all")
    return response.json()

@app.get("/countries/{country_code}")
async def get_countries_by_code(country_code: str, request: Request):
    url_with_code = "https://restcountries.com/v3.1/alpha/" + country_code
    requests_client = request.app.requests_client
    response = await requests_client.get(url_with_code)
    return response.json()


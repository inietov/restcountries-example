from fastapi import APIRouter, HTTPException, Request
from app.core.database import cursor, connection, populate_database
import json

router = APIRouter()

@router.get("/countries")
async def get_countries(size: int, page: int, request: Request):
    table_count = cursor.execute("select count(name) from countries").fetchone()[0]

    if table_count == 0:
        await populate_database(request)

    limit = size
    offset = (page - 1) * limit

    result = cursor.execute("SELECT * FROM countries LIMIT ? OFFSET ?", (limit, offset))

    return result.fetchall()

@router.get("/countries/{country_code}")
async def get_countries_by_code(country_code: str, request: Request):
    url_with_code = "https://restcountries.com/v3.1/alpha/" + country_code
    requests_client = request.app.requests_client
    response = await requests_client.get(url_with_code)
    return response.json()

@router.get("/regions")
async def get_regions(request: Request):
    table_count = cursor.execute("select count(name) from countries").fetchone()[0]

    if table_count == 0:
        await populate_database(request)

    result = cursor.execute("SELECT json_extract(data, '$.region') as region, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.region')")
    return  result.fetchall()

@router.get("/languages")
async def get_languages(request: Request):
    table_count = cursor.execute("select count(name) from countries").fetchone()[0]

    if table_count == 0:
        await populate_database(request)

    result = cursor.execute("SELECT json_extract(data, '$.languages') as languages, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.languages')")
    return  result.fetchall()

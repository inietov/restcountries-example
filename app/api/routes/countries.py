from fastapi import APIRouter, HTTPException, Request
from app.core.database import cursor, connection
import json

router = APIRouter()

@router.get("/countries")
async def get_countries(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get("https://restcountries.com/v3.1/all")
    return response.json()

@router.get("/countries/{country_code}")
async def get_countries_by_code(country_code: str, request: Request):
    url_with_code = "https://restcountries.com/v3.1/alpha/" + country_code
    requests_client = request.app.requests_client
    response = await requests_client.get(url_with_code)
    return response.json()

@router.get("/regions")
async def get_regions(request: Request):
    requests_client = request.app.requests_client
    
    table_count = cursor.execute("select count(name) from countries").fetchone()[0]

    print (table_count)
    if table_count == 0:
        response = await requests_client.get("https://restcountries.com/v3.1/all")
        data_countries = response.json()
        
        for country in data_countries:
            country_name = json.dumps(country["name"])
            country_data = json.dumps(country)
            cursor.execute("INSERT INTO countries VALUES(?, ?)", (country_name, country_data))
            connection.commit()

    result = cursor.execute("SELECT json_extract(data, '$.region') as region, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.region')")
    return  result.fetchall()

@router.get("/languages")
async def get_languages(request: Request):
    requests_client = request.app.requests_client
    
    table_count = cursor.execute("select count(name) from countries").fetchone()[0]

    if table_count == 0:
        response = await requests_client.get("https://restcountries.com/v3.1/all")
        data_countries = response.json()
        
        for country in data_countries:    
            country_name = json.dumps(country["name"])
            country_data = json.dumps(country)
            cursor.execute("INSERT INTO countries VALUES(?, ?)", (country_name, country_data))
            connection.commit()

    result = cursor.execute("SELECT json_extract(data, '$.languages') as languages, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.languages')")
    return  result.fetchall()

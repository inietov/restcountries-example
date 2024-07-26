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

@app.get("/regions")
async def get_regions(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get("https://restcountries.com/v3.1/all")
    data_countries = response.json()

    connection = sqlite3.connect("thisdot_example.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS countries(name text, data text)")
    
    for country in data_countries:
        country_name = json.dumps(country["name"])
        country_data = json.dumps(country)
        cursor.execute("INSERT INTO countries VALUES(?, ?)", (country_name, country_data))
        connection.commit()

    result = cursor.execute("SELECT json_extract(data, '$.region') as region, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.region')")
    return  result.fetchall()

@app.get("/languages")
async def get_languages(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get("https://restcountries.com/v3.1/all")
    data_countries = response.json()

    connection = sqlite3.connect("thisdot_example.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS countries(name text, data text)")

    for country in data_countries:
        country_name = json.dumps(country["name"])
        country_data = json.dumps(country)
        cursor.execute("INSERT INTO countries VALUES(?, ?)", (country_name, country_data))
        connection.commit()

    result = cursor.execute("SELECT json_extract(data, '$.languages') as languages, group_concat(json_extract(name, '$.common')) AS countries FROM countries GROUP BY json_extract(data, '$.languages')")
    return  result.fetchall()

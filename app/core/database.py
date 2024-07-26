from fastapi import Request
import sqlite3
import json

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS countries(name text, data text)")

async def populate_database(request: Request):
    requests_client = request.app.requests_client

    response = await requests_client.get("https://restcountries.com/v3.1/all")
    data_countries = response.json()
        
    for country in data_countries:    
        country_name = json.dumps(country["name"])
        country_data = json.dumps(country)
        cursor.execute("INSERT INTO countries VALUES(?, ?)", (country_name, country_data))
        connection.commit()
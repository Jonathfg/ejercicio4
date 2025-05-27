import os
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from utils.api_client import geocode_city, fetch_weather
from utils.report_generator import (
    create_dataframe,
    generate_csv,
    generate_excel,
    generate_pdf,
)

app = FastAPI(title="Weather API - Open Meteo", version="1.0")

@app.get("/weather/{city}")
async def get_weather(city: str):
    try:
        lat, lon = geocode_city(city)
        data = await fetch_weather(lat, lon)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data

@app.get("/weather/{city}/csv")
async def weather_csv(city: str):
    data = await get_weather(city)
    df = create_dataframe(data["records"])
    buffer = generate_csv(df)
    return StreamingResponse(buffer, media_type="text/csv",
                            headers={"Content-Disposition": f"attachment; filename=weather_{city}.csv"})

@app.get("/weather/{city}/excel")
async def weather_excel(city: str):
    data = await get_weather(city)
    df = create_dataframe(data["records"])
    buffer = generate_excel(df)
    return StreamingResponse(buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=weather_{city}.xlsx"}
    )

@app.get("/weather/{city}/pdf")
async def weather_pdf(city: str):
    data = await get_weather(city)
    df = create_dataframe(data["records"])
    buffer = generate_pdf(df)
    return StreamingResponse(buffer, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=weather_{city}.pdf"})
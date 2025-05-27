import os
import httpx
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_city(city: str) -> tuple[float, float]:
    """Convierte nombre de ciudad en (lat, lon) usando geopy Nominatim."""
    geolocator = Nominatim(user_agent="weather_api_app")
    try:
        location = geolocator.geocode(city)
    except GeocoderServiceError as e:
        raise RuntimeError(f"Error en geocoding: {e}")
    if not location:
        raise ValueError(f"Ciudad no encontrada: {city}")
    return location.latitude, location.longitude

async def fetch_weather(latitude: float, longitude: float) -> dict:
    """Llama a Open Meteo y devuelve JSON con hourly data."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,rain",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(OPEN_METEO_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
    # Extrae y reorganiza datos
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    hums = data["hourly"]["relative_humidity_2m"]
    rains = data["hourly"]["rain"]
    records = [
        {"time": t, "temperature": temp, "humidity": hum, "rain": rain}
        for t, temp, hum, rain in zip(times, temps, hums, rains)
    ]
    return {"city": data.get("timezone", ""), "records": records}
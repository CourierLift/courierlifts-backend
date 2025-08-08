
import httpx
from ..config import settings

# Minimal stub: if OPENWEATHER_API_KEY missing, we return None (no surcharge applied)
async def fetch_weather_code(lat: float, lon: float) -> int | None:
    if not settings.OPENWEATHER_API_KEY:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": settings.OPENWEATHER_API_KEY}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if data.get("weather"):
            return data["weather"][0].get("id")
        return None

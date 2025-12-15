from __future__ import annotations
from datetime import date
import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Москва": {"lat": 55.7558, "lon": 37.6173, "tz": "Europe/Moscow"},
    "Самара": {"lat": 53.1959, "lon": 50.1008, "tz": "Europe/Samara"},
}

def fetch_forecast_for_tomorrow(city: str, tomorrow: date) -> dict:
    c = CITIES[city]
    params = {
        "latitude": c["lat"],
        "longitude": c["lon"],
        "hourly": "temperature_2m,precipitation,windspeed_10m,winddirection_10m",
        "timezone": c["tz"],
        "start_date": tomorrow.isoformat(),
        "end_date": tomorrow.isoformat(),
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    data["_meta"] = {"city": city, "forecast_date": tomorrow.isoformat()}
    return data

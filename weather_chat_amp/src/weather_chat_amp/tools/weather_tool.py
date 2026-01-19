import requests

def weather_by_city(city: str) -> str:
    """Return current weather for a city using Open-Meteo (no API key required)."""

    # 1) Geocoding (city -> lat/lon)
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = requests.get(geo_url, params={"name": city, "count": 1}, timeout=20)
    geo_resp.raise_for_status()
    geo_data = geo_resp.json()

    if not geo_data.get("results"):
        return f"City '{city}' could not be found."

    loc = geo_data["results"][0]
    lat = loc["latitude"]
    lon = loc["longitude"]
    name = loc.get("name", city)
    country = loc.get("country", "")

    # 2) Forecast (lat/lon -> current)
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=20,
    )
    weather_resp.raise_for_status()
    weather_data = weather_resp.json()

    current = weather_data.get("current", {})
    temp = current.get("temperature_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    time = current.get("time", "")

    return (
        f"Weather in {name}, {country}:\n"
        f"🌡 Temperature: {temp}°C\n"
        f"💨 Wind Speed: {wind} m/s\n"
        f"🕒 Time: {time}"
    )

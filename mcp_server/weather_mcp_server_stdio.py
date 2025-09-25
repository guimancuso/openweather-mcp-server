import os
import dotenv
import requests
from fastmcp import FastMCP

mcp = FastMCP("OpenWeatherMCP")

dotenv.load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/"

@mcp.tool()
async def get_current_temperature(city: str) -> dict:
    """Get current weather temperature and conditions for a specific city"""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    response = requests.get(url=f"{OPENWEATHER_URL}weather", params=params)
    return response.json()

@mcp.tool()
async def get_weather_forecast(city: str) -> dict:
    """Get 5-day weather forecast with 3-hour intervals for a specific city"""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    response = requests.get(url=f"{OPENWEATHER_URL}forecast", params=params)
    return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
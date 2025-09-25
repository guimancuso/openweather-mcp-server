import os
import dotenv
import requests
from fastmcp import FastMCP

mcp = FastMCP("OpenWeatherMCP")

dotenv.load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/"

@mcp.tool()
async def buscar_temperatura_atual(city: str) -> dict:
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    response = requests.get(url=f"{OPENWEATHER_URL}weather", params=params)
    return response.json()

@mcp.tool()
async def buscar_previsao_tempo(city: str) -> dict:
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    response = requests.get(url=f"{OPENWEATHER_URL}forecast", params=params)
    return response.json()

if __name__ == "__main__":
    # HTTP transport rodando na porta 8000
    mcp.run(transport="http", port=8000, host="0.0.0.0")
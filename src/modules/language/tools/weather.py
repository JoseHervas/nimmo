import sys, os
from langchain.tools import tool
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.weather import get_weather_forecasts

class SearchInput(BaseModel):
    location: str = Field(description="should be a city name", default="cardona")

@tool("weather_forecast", return_direct=False, args_schema=SearchInput)
def weather_forecast(city: str) -> str:
    """Checks the weather forecast for the given city."""
    weather_data = get_weather_forecasts(city)
    return weather_data

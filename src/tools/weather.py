import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field

cwb_token = os.getenv('CWB_TOKEN', None)


class WeatherDataInput(BaseModel):
    """Get weather data input parameters."""
    location_name: str = Field(...,
                               description="you will be given the location of the destination of a trip and you should find the weather of this location")

    date: str = Field(...,
                            description="you will be given the location date of a trip and you should find the weather of this location")
    days: str = Field(...,
                            description="you will be given the duration of a trip and you should find the weather of this location")

class WeatherDataTool(BaseTool):
    name = "get_weather_data"
    description = "Get the weather data for trip destination location"

    def _run(self,  location_name: str, date:str, days: str):
        weather_data_results = get_weather_data(
            location_name, date, days)

        return weather_data_results

    def _arun(self, location_name: str, date:str, days: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = WeatherDataInput


def get_weather_data(location_name=None,  date=None, days=None):
    
    WEATHER_API_KEY = "1a9ee46429d74cf9b09192315231909 "

    """Get the weather forecast for the given location."""
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location_name}&dt={date}&days={days}")

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

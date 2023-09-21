import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field


class WeatherDataInput(BaseModel):
    """Get weather data input parameters."""
    location_name: str = Field(...,
                               description="you will be given the location of the destination of a trip and you should find the weather of this location")
    days: str = Field(...,
                            description="you will be given the duration of a trip and you should find the weather of destination location for a given stay days")

class WeatherDataTool(BaseTool):
    name = "get_weather_data"
    description = "Get the weather data for trip destination location note stay duration should be entered also"

    def _run(self,  location_name: str, days: str):
        weather_data_results = get_weather_data(
            location_name, days)

        return weather_data_results

    def _arun(self, location_name: str, days: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = WeatherDataInput


def get_weather_data(location_name=None, days=None):
    
    WEATHER_API_KEY = "1a9ee46429d74cf9b09192315231909 "

    """Get the weather forecast for the given location."""
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location_name}&days={days}")

    if response.status_code == 200:
        
        day_weather = []
        for weather in response["forecast"]["forecastday"]:
            day_weather.append(weather["day"])
            
        return str(day_weather)
    else:
        return response.status_code

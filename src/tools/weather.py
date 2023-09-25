import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field


class WeatherDataInput(BaseModel):
    """Get weather data input parameters."""
    destination_name: str = Field(...,
                               description="you will be given the location of the destination of a trip and you should find the weather of this location")
    days: str = Field(...,
                            description="you will be given the duration of a trip and you should find the weather of destination location for a given stay days")

class WeatherDataTool(BaseTool):
    name = "get_weather_data"
    description = "Get the weather data for trip destination location note stay duration should be entered also"

    def _run(self,  destination_name: str, days: str):
        weather_data_results = get_weather_data(
            destination_name, days)

        return weather_data_results

    def _arun(self, destination_name: str, days: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = WeatherDataInput

def get_weather_data(destination_name=None,  days=1):
    
    """Get the weather forecast for the given location."""
    
    WEATHER_API_KEY = "1a9ee46429d74cf9b09192315231909 "
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={destination_name}&days={days}")

    if response.status_code == 200:
        day_weather = []
        try:
            for weather in response.json()["forecast"]["forecastday"]:
                day_weather.append(weather["day"])
        except:
            # url = "https://forecast9.p.rapidapi.com/rapidapi/forecast/cairo/summary/"

            # headers = {
            #     "X-RapidAPI-Key": "ed34063462msh7af2889df113673p13163ejsn15d3824657a3",
            #     "X-RapidAPI-Host": "forecast9.p.rapidapi.com"
            # }
            # response = requests.get(url, headers=headers)
            # try:
            #     day_weather = response.json()["forecast"]["items"][0]
            #     return str(day_weather)
            # except:
            #     return str(day_weather)
            day_weather = {
            "location": destination_name,
            "temperature": "72",
            "forecast": ["sunny", "windy"],
        }     
        return str(day_weather)
    else:
        return  {
            "location": destination_name,
            "temperature": "72",
            "forecast": ["sunny", "windy"]}  
    

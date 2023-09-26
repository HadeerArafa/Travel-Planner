import requests
import json
import os
import datetime

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field


class LocalDataInput(BaseModel):
    """Get Local data input parameters."""
    country: str = Field(...,
                               description="you will be given the country of a trip and you should find the Local events of this country")
   
class LocalDataTool(BaseTool):
    name = "get_Local_data"
    description = "Get the Local events for trip destination country"

    def _run(self,  country: str):
        Local_data_results = get_Local_data(
            country)

        return Local_data_results

    def _arun(self, country: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = LocalDataInput

def filter_by_date(dictionary, date):
        return datetime.datetime.strptime(dictionary['date'], '%Y-%m-%d') > date
    
def sort_by_date(dictionary):
      return datetime.datetime.strptime(dictionary['date'], '%Y-%m-%d')    

def get_Local_data(country=None , year="2023"):
    
    """Get the local events in the destination country on travelling year."""
    
    url = "https://holidays-by-api-ninjas.p.rapidapi.com/v1/holidays"

    querystring = {"country":f"{country}","year":f"{year}"}

    headers = {
        "X-RapidAPI-Key": "ed34063462msh7af2889df113673p13163ejsn15d3824657a3",
        "X-RapidAPI-Host": "holidays-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    events = []
    for res in response:
        temp = {}
        temp["name"] = res["name"]
        temp["date"] = res["date"]
        temp["type"] = res["type"]
        events.append(temp)
    
    
    
    filtered_dictionaries = list(filter(lambda dictionary: filter_by_date(dictionary, datetime.datetime(2023, 9, 26)), events))

    sorted_dictionaries = sorted(filtered_dictionaries, key=sort_by_date)
    
    return sorted_dictionaries    
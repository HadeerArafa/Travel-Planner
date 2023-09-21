import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field



class HotelDataInput(BaseModel):
    """Get Hotel data input parameters."""
    location: str = Field(...,
                               description="you will be given the location of the destination of a trip where you should find a hotel")
    checkin: str = Field(...,
                               description="you will be given the checkin date of a trip and you should find a Hotel ")
    checkout: str = Field(...,
                               description="you will be given the checkout date of a trip and you should find a Hotel")
    adults: str = Field(...,
                               description="you will be given number of adults of a trip and you should find a Hotel ")


class HotelDataTool(BaseTool):
    name = "get_Hotel_data"
    description = "you will be given the location, checkin date, checkout date and number of adults you should Get the Hotel data for trip destination location only when the ueser provied all the requred data"

    def _run(self,  location: str, checkin: str, checkout: str, adults=1):
        Hotel_data_results = get_Hotel_data(
                            location,
                            checkin,
                            checkout,
                            adults)

        return Hotel_data_results

    def _arun(self,location:str,checkin:str,checkout:str,adults=1):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = HotelDataInput


def get_Hotel_data(location=None,checkin=None,checkout=None,adults=1 ):

    url = "https://airbnb13.p.rapidapi.com/search-location"

    querystring = {"location":{location},"checkin":{checkin},"checkout":{checkout},"adults":{adults},"currency":"USD"}

    headers = {
        "X-RapidAPI-Key": "ed34063462msh7af2889df113673p13163ejsn15d3824657a3",
        "X-RapidAPI-Host": "airbnb13.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    all_totels = []
    for res in response.json()["results"]:
        keys = res.keys()
        temp = {}
        if "name" in keys:
            temp["name"] = res["name"] 
        if "bathrooms" in keys:
            temp["bathrooms"] = res["bathrooms"] 
        if "bedrooms" in keys:   
            temp["bedrooms"] = res["bedrooms"] 
        if "beds" in keys:
            temp["beds"] = res["beds"] 
        if "city" in keys:
            temp["city"] = res["city"] 
        if "persons" in keys:
            temp["persons"] = res["persons"] 
        if "rating" in keys:
            temp["rating"] = res["rating"] 
        if "address" in keys:
            temp["address"] = res["address"] 
        if "price" in keys:
            temp["price"] = res["price"] 
        all_totels.append(temp) 
   

    if response.status_code == 200:
        return str(all_totels)
    else:
        return response.status_code

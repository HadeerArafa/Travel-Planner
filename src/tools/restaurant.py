import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field

def get_restaurant_data(restaurants):
    for restaurant in restaurants:
        location_id  = restaurant["location_id"]
        
        url = "https://travel-advisor.p.rapidapi.com/restaurants/get-details"

        querystring = {"location_id":f"{location_id}","currency":"USD","lang":"en_US"}

        headers = {
            "X-RapidAPI-Key": "ed34063462msh7af2889df113673p13163ejsn15d3824657a3",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()
        if "description" in response:
            restaurant["description"] = response["description"]
        
        if "ranking" in response:
            restaurant["ranking"] = response["ranking"]  
        
        if "rating" in response:
            restaurant["rating"] = response["rating"]    
            
        if "phone" in response:
            restaurant["phone"] = response["phone"]    
        
        if "website" in response:
            restaurant["website"] = response["website"]    
        if "price" in response:
            restaurant["price"] = response["price"]  
    return restaurants        
                
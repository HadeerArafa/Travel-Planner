import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field

def get_data(destination):
    
    results = {}
    
    url = "https://travel-advisor.p.rapidapi.com/locations/search"

    querystring = {"query":f"{destination}","limit":"20","offset":"0","units":"km","currency":"USD","sort":"relevance","lang":"en_US"}

    headers = {
        "X-RapidAPI-Key": "ed34063462msh7af2889df113673p13163ejsn15d3824657a3",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        response = response.json()
        for d in response["data"]:
            temp = {}
            result_object = d["result_object"]
            if "location_id" in result_object.keys():
                temp["location_id"] = result_object["location_id"]
            
            if "name" in result_object.keys():
                temp["name"] = result_object["name"]
            
            if "geo_description" in result_object.keys():
                temp["geo_description"] = result_object["geo_description"]
            
            if "num_reviews" in result_object.keys():
                temp["num_reviews"] = result_object["num_reviews"]
            
            if "address" in result_object.keys():
                temp["address"] = result_object["address"]
            
            if "establishment_types" in result_object.keys():
                temp["establishment_types"] = result_object["establishment_types"][0]["name"]

            if "review_snippet" in d.keys():
                temp["review"] = d["review_snippet"]["snippet"]
            result_type = d["result_type"] 
            if result_type not in results.keys():
                results[f"{result_type}"] = [temp]
            else :
                results[f"{result_type}"] = results[f"{result_type}"] + [temp]
        return results
    else :
        return results    
import requests
import json
import os

from langchain.tools import BaseTool
from langchain.agents import AgentType
from typing import Optional, Type
from pydantic import BaseModel, Field


def get_flights(departure, destination , date, adults=1, classtype="ECONOMY"):
    departure_airport_key = ""
    destination_airport_key=""
    all_avaliable_flights = []
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"

    querystring = {"query":f"{departure}"}

    headers = {
    'X-RapidAPI-Key': 'b911cca1fcmsh1120345a7e835a3p1818ccjsneb40da94ab77',
    'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com'
  }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print("responseflight" ,response )
    if response["status"] == True:
        departure_airport_key = response["data"][0]["airportCode"]
        print("departure_airport_key" ,departure_airport_key )
        
    
    querystring = {"query":f"{destination}"}

    headers = {
        "X-RapidAPI-Key": "b911cca1fcmsh1120345a7e835a3p1818ccjsneb40da94ab77",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    if response["status"] == True:
        destination_airport_key = response["data"][0]["airportCode"]
        print("destination_airport_key" ,destination_airport_key )
        
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"

    querystring = {"sourceAirportCode":f"{departure_airport_key}",
                   "destinationAirportCode":f"{destination_airport_key}",
                   "date":f"{date}",
                   "itineraryType":"ONE_WAY",
                   "sortOrder":"PRICE",
                   "numAdults":f"{adults}",
                   "numSeniors":"0",
                   "classOfService": f"{classtype}",
                   "pageNumber":"1",
                   "currencyCode":"USD"}

    headers = {
        "X-RapidAPI-Key": "b911cca1fcmsh1120345a7e835a3p1818ccjsneb40da94ab77",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print("final response")
    if response["status"] == True:
        for flight in response["data"]["flights"]:
            temp = {}
            legs = flight["segments"][0]["legs"][0]
            temp["departureDateTime"] = legs["departureDateTime"]
            temp["arrivalDateTime"] = legs["arrivalDateTime"]
            temp["classOfService"] = legs["classOfService"]
            temp["flightNumber"] = legs["flightNumber"]
            purchase = flight["purchaseLinks"][0]
            temp["currency"] = purchase["currency"]
            temp["totalPrice"] = purchase["totalPrice"]
            all_avaliable_flights.append(temp)    
    
    return all_avaliable_flights        
            
          
            
        
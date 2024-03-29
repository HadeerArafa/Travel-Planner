import os
import importlib
import sys
import json
import pandas as pd
import streamlit as st
from io import BytesIO
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
import openai
import time
from tools.weather import get_weather_data
from tools.hotel import get_Hotel_data
from tools.local import get_Local_data
import re
from serpapi import GoogleSearch
from tools.flight import get_flights
from tools.destenation_info import get_data
from tools.restaurant import get_restaurant_data

def reload_module(module_name):
    """For update changes
    made to modules in localhost (press r)"""


layout_module = reload_module("modules.layout")
utils_module = reload_module("modules.utils")
sidebar_module = reload_module("modules.sidebar")


st.set_page_config(
    layout="wide",
    page_icon="💬",
    page_title="WanderlustAI Inc AI assistant | Chat-Bot 🤖",
)

layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header()

user_api_key = utils.load_api_key()
os.environ["OPENAI_API_KEY"] = user_api_key
openai.api_key =user_api_key

st.markdown(
    """
    <style>
    .css-1c7y2kd {
        /* Add your custom styles here */
        display: flex;
        flex-direction: row-reverse;
        text-align : end;
        
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def final_response ():
    if st.session_state.call_api == False:
        print("calling api")
        msg = [{
        "role": "user",
        "content": ''' summarize the conversation you need to extract information about the trip 
        what you need to extract is  departure location ,destination location , departure country, destination country, travel date, travel year
        how long you are they ganne to stay , use travel date and stay_days to calc when they will return,
        how many paople gonne travel, trip budget, transporter , activit types and interests ,cuisine type
        the output should be "json" formate without any additinal context like this :
        {
            departure : departure location
            destination : destination location
            departure_country = departure country
            destination_country : destination country
            travel_date : travel date
            travel_year : travel year date
            stay_days : how long you are they ganne to stay
            return_date : use travel date and stay_days to calc when they will return
            people_to_travel : how many paople gonne travel
            budget : trip budget
            transporter : transporter
            activity : activit types and interests
            cuisine : cuisine type
            additional : anything alse they want to add any kind of activity or anything you should consider
        }
        '''
        }
        ]
    
        all_msgs =  [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages] +msg
        
        response = openai.ChatCompletion.create( model="gpt-3.5-turbo",
                                                messages=all_msgs,  
                                                            )
        
        message_placeholder = st.empty()
        full_response = ""
        wait_msg = " I'm cooking up a personalized trip plan for you right now. Stay tuned for the delicious results!" 
        token = re.split(r" " "| ! | , | ? ", wait_msg)    
        for part in token:
            full_response += part+" "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        print("first response" ,response )
        content = response.choices[0]["message"]["content"]
        data_dict = json.loads(content)
        print("data_dict" , data_dict)
        weather = {}
        try:
            weather = get_weather_data(destination_name=data_dict["destination"] , days=data_dict["stay_days"])
            print("wather" , weather)
        except:
            print("failed to get weather data")
        local = {}
        try:        
            local = get_Local_data(country=data_dict["destination_country"], year=data_dict["travel_year"], travel_date=data_dict["travel_date"],leave_date=data_dict["return_date"])
            print("local" , local)
        except:
            print("failed to get local events")
        hotal = {}
        try:        
            hotal = get_Hotel_data(location=data_dict["destination"], checkin=data_dict["travel_date"], checkout=data_dict["return_date"], adults=data_dict["people_to_travel"])
            print("hotal" , hotal)
        except:
            print("fialed to get hotal ")   
        flight = {}
        try:        
            flight = get_flights(departure=data_dict["departure_country"], destination=data_dict["destination_country"] , date=data_dict["travel_date"],adults=data_dict["people_to_travel"])
            print("flight" , flight)
        except:
            print("fialed to get flight")
        
        destination_data = {}    
        try:        
            destination_data = get_data(data_dict["destination"])
            destination_data["geos"] = []
            destination_data["lodging"] = [] # no need for them
            print("destination_data" , destination_data)
        except:
            print("fialed to get destination_data ")
            
        
        if "restaurants" in destination_data.keys() :
            restaurants = destination_data["restaurants"]        
            try:
                res = get_restaurant_data(restaurants)   
                destination_data["restaurants"]  = res
                print("destination_data_restaurants" , destination_data["restaurants"])
            except:
                print("destination_data_restaurants" , destination_data["restaurants"])
        
        msg = [{
        "role": "user",
        "content": f''' you are ai assistant and you should help user plan for they trip 
        given the user departure {data_dict["departure"]} , user destination {data_dict["destination"]}
        travel date {data_dict["travel_date"]} , stay duration {data_dict["stay_days"]}
        how many people are going to travel {data_dict["people_to_travel"]} , budget {data_dict["budget"]}
        transporter they are going to use in the destination {data_dict["transporter"]}
        activity types and interests they prefere {data_dict["activity"]}
        cuisine type they prefer{data_dict["cuisine"]}
        anything alse you they want to add a note any kind of activity or anything you should consider {data_dict["additional"]}
        you should organize the trip considering they budget and the wather in the destinatio {weather}
        and you should use flight data to give them avaliavle optional of the flights {flight} and if there is no avliable flights tell them that
        and you should sugest hotel for them from this data{hotal} to stay and give them all the avaliable information about the hotel specially the price and you should consider the budget while choising the hotels
        and you should tell them all the local event while they time in the trip using this data {local}
        and there is a destination information {destination_data} use it to sugest a resturant and any activeties they can do
        note to always provied them with all the avaliable data like price and phone number and you should consider the budget for all you sugestion 
        ------
        Format your response using Markdown. Use headings, subheadings, bullet points, and bold to organize the information.
        give them information about the weather , thing to do while there are in the trip, Safety & Local Guidelines for the destination
        and you should provide essential phrases or translations in the local language of the vacation spot 
        always give them the cheapest options and provied them with all the necessry detailes 
        --------
        '''
        }
        ]
        
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=msg)
        
        print("second response" , response) 
        # message_placeholder = st.empty()
        # full_response = ""
        msg_of_response = str(response.choices[0]["message"]["content"]) 
        # token = re.split(r" " "| ! | , | ? ", msg)    
        # for part in token:
        #     full_response += part+" "
        #     time.sleep(0.02)
        #     message_placeholder.markdown(full_response + "▌")
        
        
        msg = [{
        "role": "user",
        "content": f''' you are ai assistant and you should help user plan for they trip
        Format your final response using Markdown. Use headings, subheadings, bullet points, and bold to organize the information as you
        are required to give detials about what user should do eveyday in they trip. your output should be like day1 .... , day2 ...."
        Generate a personalized travel itinerary for a trip 
        given the weather data, hotel options local envents  ,resturant and thing to do from {response.choices[0]["message"]["content"]}
        you also given the user departure {data_dict["departure"]} , user destination {data_dict["destination"]}
        travel date {data_dict["travel_date"]} , stay duration {data_dict["stay_days"]}
        how many people are going to travel {data_dict["people_to_travel"]} , budget {data_dict["budget"]}
        transporter they are going to use in the destination {data_dict["transporter"]}
        activity types and interests they prefere {data_dict["activity"]}
        cuisine type they prefer{data_dict["cuisine"]}
        anything alse you they want to add a note any kind of activity or anything you should consider {data_dict["additional"]}
        Once the initial plan is presented, users should be able to ask for changes ("Add more beach days" or "Suggest a local festival"), and the model should dynamically adjust the itinerary
        give the user a detailed plan for each day what should he do and where should he go for each day in the trip dived each day to moring afternoon and eveing
        '''
        }
        ]
        
        response = openai.ChatCompletion.create( 
                                                            model="gpt-3.5-turbo",
                                                                messages=msg,
                                                            )
        message_placeholder = st.empty()
        full_response = ""
        msg = msg_of_response + "\n " + str(response.choices[0]["message"]["content"]) 
        token = re.split(r" " "| ! | , | ? ", msg)    
        for part in token:
            full_response += part+" "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})  
        st.session_state.init_plan = [{"role": "assistant", "content": full_response}]
        
        print("third response" , response) 
        st.session_state.call_api = True            
        return response  

    else:
        print("now i am here" )
        all_msgs = Utilities.basic_msg + st.session_state.init_plan + [ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-4:]]
        response = openai.ChatCompletion.create( 
                                                model="gpt-3.5-turbo",
                                                messages=all_msgs)
        
        message_placeholder = st.empty()
        full_response = ""
        msg = str(response.choices[0]["message"]["content"]) 
        token = re.split(r" " "| ! | , | ? ", msg)    
        for part in token:
            full_response += part+" "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response}) 
        
        return response                                               
        
functions = [
        {
            "name": "final_response",
            "description": """
           this function will be used to generate response after the user has entered all it' s data and there is no more questions
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "string",
                        "description": "all the messages between the user and the ai assestant ",
                    },
                },
                "required": ["messages"],
            },
        } 
        
    ]

if not user_api_key:
    layout.show_api_key_missing()

else:
    st.session_state.setdefault("reset_chat", False)

    sidebar.about()

    if "messages" not in st.session_state:
        st.session_state.messages = [{
             "role":"assistant",
                "content" :"I am WanderlustAI Inc AI assistant and i'm gonne help you plan for your trip can i start by getting your name"
        }]
        st.session_state.call_api = False
    
    
    for idx, message_ in enumerate(st.session_state.messages):
        with st.chat_message(message_["role"]):
            st.markdown(message_["content"])
    
    if prompt := st.chat_input(""):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
            
        time.sleep(1)     
        
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            all_msgs = Utilities.basic_msg +[ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            response = openai.ChatCompletion.create( 
                                                        model="gpt-3.5-turbo",
                                                            messages=all_msgs,
                                                            functions=functions,
                                                            function_call="auto",  # auto is default, but we'll be explicit
                                                            # stream=True,    
                                                        )
            print("responseeeeeeeeeee" , response)
            if "function_call" in response["choices"][0]["message"].keys():
                available_functions = {
                    "final_response": final_response,
                }  # only one function in this example, but you can have multiple
                function_name = response["choices"][0]["message"]["function_call"]["name"]
                if(function_name in available_functions.keys()):
                    fuction_to_call = available_functions[function_name]
                    response = fuction_to_call(
                        # messages=function_args.get("messages"),
                    )
                else :
                    response = openai.ChatCompletion.create( 
                                                        model="gpt-3.5-turbo",
                                                            messages=all_msgs,
                                                        )   
                    msg = str(response.choices[0]["message"]["content"]) 
                    token = re.split(r" " "| ! | , | ? ", msg)    
                    for part in token:
                        full_response += part+" "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            
                    st.session_state.messages.append({"role": "assistant", "content": full_response}) 
                 
            else :    
                msg = str(response.choices[0]["message"]["content"]) 
                token = re.split(r" " "| ! | , | ? ", msg)    
                for part in token:
                    full_response += part+" "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
           
                st.session_state.messages.append({"role": "assistant", "content": full_response})    
    

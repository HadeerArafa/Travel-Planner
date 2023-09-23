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


def search_flight(q):
    search = GoogleSearch({
    "q": {q}, 
    "api_key": "43b6459e95cf735c6e48cd6756e7d36f58ab04b60554cbb39f4e58367620111c"
    })
    result = search.get_dict()
    return result
    

functions = [
        {
            "name": "search_flight",
            "description": """
            use it to search for best airport to travel from departure location to destination location or
            after asking the user :
            --------
            AI: What is your departure location ?
            user : cairo
            AI : And what is yout distination location 
            user : paris
            AI : when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?
            user 29-9-2023 
            --------
            call search with parameters (q = flight schedules to travel from {cairo} to {paris} in {29-9-2023} )
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "the quary that will be used in search should be something like flight schedules to travel from {cairo} to {paris} in {29-9-2023}",
                    },
                },
                "required": ["q"],
            },
        } ,
        {
            "name": "get_weather_data",
            "description": """
            this function will find the forecast of distination for given number of days 
            --------
            after getting the user destination and how many days he will speand you need to find the weather of the destination 
            --------
            AI : And what is yout distination location 
            user : paris
            .
            .
            .
            .
            AI : how long you are ganne to stay
            user : 5 days
            ---------
            call get_weather_data with parameters (destination_name = paris , days= 5)
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "destination_name": {
                        "type": "string",
                        "description": "The city and state of the destination, e.g. San Francisco, CA",
                    },
                    "days": {"type": "string", 
                             "description": "how many days the user will speend in the trip"},
                },
                "required": ["destination_name" , "days"],
            },
        },
        
        {
            "name": "get_Local_data",
            "description": """
            this function will get the local events of the destination on the travel year :
            after asking the user :
            --------
            AI : And what is yout distination location 
            user : paris
            AI : Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?
            user : 26-9-2023
            --------
            call get_Local_data with parameters (country=paris , year=2023)
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "The country of the destination, e.g. Egypt, Paris",
                    },
                    "year": {"type": "string", 
                             "description": "the year when the user will travel, e.g. 2023, 2024"},
                },
                "required": ["country" , "year"],
            },
        },
        
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
                                                        model="gpt-3.5-turbo-0613",
                                                            messages=all_msgs,
                                                            functions=functions,
                                                            function_call="auto",  # auto is default, but we'll be explicit
                                                            # stream=True,    
                                                        )
            print("response" ,response)
            if "function_call" in response["choices"][0]["message"].keys():
                available_functions = {
                    "get_weather_data": get_weather_data,
                }  # only one function in this example, but you can have multiple
                function_name = response["choices"][0]["message"]["function_call"]["name"]
                fuction_to_call = available_functions[function_name]
                function_args = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
                function_response = fuction_to_call(
                    destination_name=function_args.get("destination_name"),
                    days=function_args.get("days"),
                )
                print("function response" , function_response)
    
                st.session_state.messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  

                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=st.session_state.messages,
                    )  
                print("second response" , response)
            msg = str(response.choices[0]["message"]["content"]) 
            print("msg",msg)
            token = re.split(r" " "| ! | , | ? ", msg)    
            for part in token:
                full_response += part+" "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
           
        st.session_state.messages.append({"role": "assistant", "content": full_response})    
    






# if int(st.session_state.count) < len(question_list):
#     if prompt := st.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         with st.chat_message("user"):
#             st.markdown(prompt)

#         time.sleep(1)

#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""
#             assistant_response = question_list[st.session_state.count]
#             for chunk in assistant_response.split():
#                 full_response += chunk + " "
#                 time.sleep(0.05)
#                 message_placeholder.markdown(full_response + "▌")
#             message_placeholder.markdown(full_response)

#         st.session_state.messages.append(
#             {"role": "assistant", "content": full_response}
#         )
#         st.session_state.count = st.session_state.count + 1


# else:
#     if prompt := st.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         time.sleep(1)

#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""
#             assistant_response = " i have no answer to that".split()
#             for chunk in assistant_response:
#                 full_response += chunk + " "
#                 time.sleep(0.05)
#                 message_placeholder.markdown(full_response + "▌")
#             message_placeholder.markdown(full_response)

#         st.session_state.messages.append(
#             {"role": "assistant", "content": full_response}
#         )
#         st.session_state.count = st.session_state.count + 1



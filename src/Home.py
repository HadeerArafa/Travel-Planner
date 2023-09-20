import os
import importlib
import sys
import pandas as pd
import streamlit as st
from io import BytesIO
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
import openai
import time
from streamlit_chat import message

msg_assistanse = [""]


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

question_list =""" [
    "Great. What is your departure location ? ",
    "And what is yout distination location",
    "Greet choise , when are you planning to travel?"
    "how long you are ganne to stay"
    "Alright , what is the budget for the trip?",
    "transporter type => car , bus ,...",
    "activit types and interests (beach, mountains, culture, adventure, etc.)",
    "cuisine type",
    "anything alse you want to add a note any kind of activity or anything i should consider"
    ] """
basic_msg = [
            {
                "role": "system",
                "content": '''you are an intelligent AI assistant that tailors vacation plans based on a user's preferences,past travels, budget, and more 
                captures essential user details: travel history, interests (beach, mountains, culture, adventure, etc.), dietary restrictions, budget, and other preferences to make informed suggestions.
                note you should just ask one question each time
                note you should use user name when he provied it 
                using a set of question 
                note you should ask one question at a time and wait for the user response to generate another response
                and after getting all the data you should then thank the user and tell them you will start to plane and you should then response "finish collectiing data" so i know you finished and i can go to next step i want you to generate these two msgs in the same time
                and here is an example of the question :
                ["What is your departure location ? ",
                "And what is yout distination location",
                "Greet choise , when are you planning to travel?"
                "Alright , what is the budget for the trip? and note all the suggession you make should consider the budget ",
                "trip duration and it's a must question to be asked and you should plan only for the given number of days",
                "transporter type you want to use when you arrive => car , bus ,...",
                "activit type and interests (beach, mountains, culture, adventure, etc.)",
                "cuisine type",]
                please rephares them and generate as much question as you need to have all the data to plan
                ''',
            
            },
            {
                "role":"assistant",
                "content" :question_list
            },
            {
                "role":"user",
                "content" :"please ask one question at a time "
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
        
    for idx, message_ in enumerate(st.session_state.messages):
        with st.chat_message(message_["role"]):
            st.markdown(message_["content"])
    

     
   
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     all_msgs = basic_msg +[ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    #     print("all_msg" , all_msgs)
    #     for response in openai.ChatCompletion.create( 
    #                                                  model="gpt-3.5-turbo",
    #                                                     messages=all_msgs,
    #                                                     stream=True,    
    #                                                 ):
    #         full_response += response.choices[0].delta.get("content", "")
    #         message_placeholder.markdown(full_response + "▌")
    #     message_placeholder.markdown(full_response)
    # st.session_state.messages.append({"role": "assistant", "content": full_response})

    
            
    if prompt := st.chat_input(""):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
            
        time.sleep(1)    
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            all_msgs = basic_msg +[ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            for response in openai.ChatCompletion.create( 
                                                        model="gpt-3.5-turbo",
                                                            messages=all_msgs,
                                                            stream=True,    
                                                        ):
                print("response", response )
                full_response += response.choices[0].delta.get("content", "")
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



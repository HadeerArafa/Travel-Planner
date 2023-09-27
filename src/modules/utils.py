import os
import pandas as pd
import streamlit as st


class Utilities:

    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #you can define your API key in .env directly
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env", icon="🚀")
        else:
            if st.session_state.api_key is not None:
                user_api_key = st.session_state.api_key
                st.sidebar.success("API key loaded from previous input", icon="🚀")
            else:
                user_api_key = st.sidebar.text_input(
                    label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key

        return user_api_key

    
    question_list =""" [
    "Great. What is your departure location ? ",
    "And what is yout distination location",
    "Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?",
    "how many paople gonne travel",
    "how long you are ganne to stay",
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
                    in the plan you should consider the weather and sujgest any local event and which airport they should talk and any near hotal and try to hightlight the budget of the activitas
                    [
                    "Great. What is your departure location ? ",
                        "And what is yout distination location",
                        "Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?",
                        "how long you are ganne to stay ",
                        "how many paople gonne travel including you",
                        "Alright , what is the budget for the trip?",
                        "transporter type you prefere to use in the trip=> car , bus ,...",
                        "activit types and interests (beach, mountains, culture, adventure, etc.)",
                        "cuisine type",
                        "anything alse you want to add a note any kind of activity or anything i should consider"]
                    please rephares them and generate as much question as you need to have all the data to plan
                    after all the question you should call the function response to generate the response
                    
                   
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


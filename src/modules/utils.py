import os
import pandas as pd
import streamlit as st

from modules.chatbot import Chatbot

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

    
    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:

            def show_csv_file(uploaded_file):
                file_container = st.expander("Your CSV file :")
                uploaded_file.seek(0)
                shows = pd.read_csv(uploaded_file)
                file_container.write(shows)

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
            
            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8")
                file_container.write(content)
            
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)

            # Show the contents of the file based on its extension
            #if file_extension == ".csv" :
            #    show_csv_file(uploaded_file)
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
            elif file_extension== ".txt" : 
                show_txt_file(uploaded_file)

        else:
            st.session_state["reset_chat"] = True

        #print(uploaded_file)
        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # Get the document embeddings for the uploaded file
            vectors = embeds.getDocEmbeds(file, uploaded_file.name)

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature,vectors)
        st.session_state["ready"] = True

        return chatbot
    
    
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
                    and after getting all the data you should then thank the user and start generate the personalized plan
                    you should call the weather function after the user enter the destination and the days they will spend in the trip
                    in the plan you should consider the weather and sujgest any local event and which airport they should talk and any near hotal and try to hightlight the budget of the activitas
                    [
                    "Great. What is your departure location ? ",
                        "And what is yout distination location",
                        "Greet choise , when are you planning to travel please provied the date in yyyy-mm-dd for better experiance?",
                        "how long you are ganne to stay => note : "this is trip duration after asking this question you should call the function get_weather_data to get the weather of the destination" ",
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


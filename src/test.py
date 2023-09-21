from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
import os
# Optionally, specify your own session_state key for storing messages
msgs = StreamlitChatMessageHistory(key="special_app_key")

memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("I am WanderlustAI Inc AI assistant and i'm gonne help you plan for your trip can i start by getting your name?")
                
    
os.environ["OPENAI_API_KEY"] = "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"

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

template = """you are an intelligent AI assistant that tailors vacation plans based on a user's preferences,past travels, budget, and more 
                captures essential user details: travel history, interests (beach, mountains, culture, adventure, etc.), dietary restrictions, budget, and other preferences to make informed suggestions.
                note you should just ask one question each time
                note you should use user name when he provied it 
                using a set of question 
                note you should ask one question at a time and wait for the user response to generate another response
                and after getting all the data you should then thank the user and tell them you will start to plane and you should then response "finish collectiing data" so i know you finished and i can go to next step i want you to generate these two msgs in the same time
                and here is an example of the question :
                [
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
                    ]
                please rephares them and generate as much question as you need to have all the data to plan but note that you have to
                only ask one question at a time

{history}
Human: {human_input}
AI: """
prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

# Add the memory to an LLMChain as usual
llm_chain = LLMChain(llm=OpenAI(), prompt=prompt, memory=memory)    


for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

            
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)
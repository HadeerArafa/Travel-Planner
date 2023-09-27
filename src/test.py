from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import tool
import streamlit as st
import os
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import AgentType
# LINE Travel Tools
from tools.weather import WeatherDataTool
from tools.hotel import HotelDataTool
from tools.local import LocalDataTool


# Optionally, specify your own session_state key for storing messages
msgs = StreamlitChatMessageHistory(key="special_app_key")

if len(msgs.messages) == 0:
    msgs.add_ai_message("I am WanderlustAI Inc AI assistant and i'm gonne help you plan for your trip can i start by getting your name?")
                
    
os.environ["OPENAI_API_KEY"] = ""

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

memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs)

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

model = OpenAI()

llm_chain = LLMChain(llm=model, prompt=prompt, memory=memory)  

search = DuckDuckGoSearchRun()

@tool
def question(qes: str) -> str: 
    """Returns the question that the model want to ask to user."""
    return qes



tools = [HotelDataTool(), LocalDataTool(),
             WeatherDataTool(),
             
             Tool( name="Search",
                func=search.run,
                description="useful when user gives you both the destination and departion and you should find avaliable travel between them both",
    ),
             Tool.from_function(
        func=question,
        name="question",
        description="use this to ask the user the question in the prompet to gather info about him for better trip planning",
        args_schema=memory
        # coroutine= ... <- you can specify an async method if desired as well
    )]


prefix = """
you are an intelligent AI assistant that tailors vacation plans based on a user's preferences,past travels, budget, and more 
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
"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

  

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)



for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

            
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    # response = llm_chain.run(prompt)
    response = agent_chain.run(prompt)
    st.chat_message("ai").write(response)
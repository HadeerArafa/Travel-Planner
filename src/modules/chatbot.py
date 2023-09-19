import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback

#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    qa_template = """
        WanderlustAI Inc. is a pioneering travel-tech company seeking to revolutionize how individuals plan their vacations. Their vision is to create an intelligent AI assistant that tailors vacation plans based on a user's preferences, past travels, budget, and more. The challenge is to utilize GPT-3.5 Turbo to produce an AI model capable of planning and optimizing a vacation itinerary with minimal user input.
        Case Questions & Tasks:
        1.	Dynamic Profile Creation:
        1.	Develop an algorithm where GPT-3.5 Turbo captures essential user details: travel history, interests (beach, mountains, culture, adventure, etc.), dietary restrictions, budget, and other preferences to make informed suggestions.
        2.	Real-time Data Integration:
        1.	Ensure the AI model can interact with real-time data sources like weather forecasts, flight schedules, hotel availability, local events, and more, to create an optimized itinerary.
        3.	Complex Query Handling:
        1.	The AI assistant should be proficient in processing multi-dimensional queries like "I want a 10-day trip, blending beach relaxation, historical sites, and a touch of adventure, under $2000."
        4.	Interactive Itinerary Adjustments:
        1.	Once the initial plan is presented, users should be able to ask for changes ("Add more beach days" or "Suggest a local festival"), and the model should dynamically adjust the itinerary.
        5.	Safety & Local Guidelines:
        1.	The chatbot should incorporate safety tips, local customs, travel restrictions, or any relevant advisories pertaining to the destination.
        6.	Multi-language Support:
        1.	While the main interaction would be in English, ensure a mechanism where the AI model can provide essential phrases or translations in the local language of the vacation spot.
        7.	Continuous Feedback Loop:
        1.	After the vacation, the AI should be able to gather feedback, learn from it, and refine future suggestions. Was the suggested hotel satisfactory? Were the local activities enjoyable? Such insights will help in tailoring future travel plans.
        8.	Budgetary Optimization:
        1.	Integrate algorithms that can suggest best-value options for accommodations, activities, and dining, ensuring users get the best experience within their specified budget.


        context: {context}
        =========
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context"])

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()


        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        #count_tokens_chain(chain, chain_input)
        return result["answer"]


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    

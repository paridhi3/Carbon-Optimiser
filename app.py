import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory

import json
 
# Load environment variables
load_dotenv()
 
# Emission factors
EMISSION_FACTORS = {
    "transport": {
        "car_gasoline": 0.21,
        "car_diesel": 0.23,
        "electric_car": 0.05,
        "bus": 0.09,
        "train": 0.04,
        "bike": 0.0,
        "walk": 0.0
    },
    "energy": {
        "electricity_avg": 0.4,
        "electricity_renewable": 0.05,
        "natural_gas": 0.19,
        "heating_oil": 0.27
    },
    "diet": {
        "beef": 5.0,
        "lamb": 4.8,
        "chicken": 1.8,
        "pork": 2.4,
        "fish": 2.0,
        "eggs": 1.6,
        "milk": 1.2,
        "cheese": 3.0,
        "lentils": 0.9,
        "beans": 1.0,
        "tofu": 1.3,
        "vegetables": 0.5
    }
}

@tool
def carbon_calculator(transport: str = "walk", distance_km: float = 0.0, energy: str = "electricity_avg", energy_kwh: float = 0.0, diet: str = "vegetables", meals_per_week: int = 0) -> str:
    """
    Calculates estimated weekly carbon footprint based on transport, energy, and diet.
    """
    
    transport_emission = EMISSION_FACTORS["transport"].get(transport, 0) * distance_km
    energy_emission = EMISSION_FACTORS["energy"].get(energy, 0) * energy_kwh
    diet_emission = EMISSION_FACTORS["diet"].get(diet, 0) * meals_per_week
    total_emission = transport_emission + energy_emission + diet_emission

    response = f"Estimated weekly carbon footprint: {total_emission:.2f} kg CO₂"

    return response
 
@tool
def suggest_alternatives(transport: str, energy: str, diet: str) -> str:
    """
    Suggests lower-emission alternatives for transport, energy, and diet.
    """
    suggestions = []
    if EMISSION_FACTORS["transport"].get(transport, 1) > 0.1:
        suggestions.append("Consider switching to public transport, biking, or walking.")
    if energy != "electricity_renewable":
        suggestions.append("Switch to renewable electricity sources if available.")
    if diet in ["beef", "lamb", "cheese"]:
        suggestions.append("Reduce red meat and dairy; try lentils, beans, or vegetables.")
    return "Suggestions:\n" + "\n".join(suggestions) if suggestions else "Your choices are already low-emission!"
 
# LLM setup
llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_END_POINT"),
    deployment_name=os.getenv("deployment_name"),
    model=os.getenv("MODEL_NAME"),
    api_version=os.getenv("API_VERSION")
)
 
# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a carbon footprint optimization assistant. "
     "Your goal is to calculate the estimated carbon footprint and help users reduce "
     "their environmental impact by analyzing their lifestyle choices and suggesting "
     "lower-emission alternatives. Be specific, data-driven, and practical."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Agent setup
tools = [carbon_calculator, suggest_alternatives]
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

#==================================================================================================

# CHAINING
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

extraction_prompt = ChatPromptTemplate.from_template("""
Extract the following details from the user input:

transport: one of {valid_transports}
distance_km: number (total weekly distance in km)
energy: one of {valid_energies}
energy_kwh: number
diet: one of {valid_diets}
meals_per_week: number

Respond ONLY in this JSON format:
{{
  "transport": ...,
  "distance_km": ...,
  "energy": ...,
  "energy_kwh": ...,
  "diet": ...,
  "meals_per_week": ...
}}

User input: {input}
""")

extraction_chain = LLMChain(
    llm=llm,
    prompt=extraction_prompt.partial(
        valid_transports=", ".join(EMISSION_FACTORS["transport"].keys()),
        valid_energies=", ".join(EMISSION_FACTORS["energy"].keys()),
        valid_diets=", ".join(EMISSION_FACTORS["diet"].keys())
    )
)

#==================================================================================================

import streamlit as st

# Set up the Streamlit chatbot UI
st.set_page_config(page_title="Carbon Chatbot", layout="centered")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

memory = st.session_state.memory
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

#==================================================================================================

st.title("♻️ Carbon Optimizer Agent")
st.write("Describe your lifestyle, and I'll estimate your carbon footprint.")

# Reset button
if st.button("🔄 Reset Chat", help="Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.pop("pending_input", None)
    memory.clear()
    st.rerun()

# Chat input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Tell me about your travel, energy, and diet habits...")

if user_input:
    with st.spinner("Thinking..."):

        if "footprint_inputs" not in st.session_state:
            st.session_state.footprint_inputs = {
                "transport": None,
                "distance_km": None,
                "energy": None,
                "energy_kwh": None,
                "diet": None,
                "meals_per_week": None
            }

        # Extract input details
        parsed_response = extraction_chain.run(input=user_input)

        try:
            parsed_data = json.loads(parsed_response)  # JSON-safe in prod: json.loads()
            for key, value in parsed_data.items():
                if value not in [None, "", "null"]:
                    st.session_state.footprint_inputs[key] = value
        except Exception as e:
            st.warning("Could not parse input. Try rephrasing.")
            st.stop()

        # response = agent_executor.invoke({"input": parsed_response})
        response = agent_executor.invoke({
         "input": f"Here are the extracted details: {parsed_response}. Also, the user said: {user_input}"
        })


        # Save chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response["output"]})


# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

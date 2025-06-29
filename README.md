# ♻️ Carbon Footprint Optimization Assistant
This project is an AI-powered assistant built using **LangChain**, **Streamlit**, and **Azure OpenAI**, designed to help users estimate and reduce their **weekly carbon footprint**. The agent interacts conversationally, calculates emissions based on transport, energy, and diet inputs, and suggests personalized low-carbon alternatives.

## 🚀 Features
- ✅ **Carbon Calculator Tool** – Estimates weekly CO₂ emissions from lifestyle choices.
- 💡 **Alternative Suggestions Tool** – Recommends greener alternatives to reduce your footprint.
- 🧠 **Conversational Memory** – Remembers facts like your name or habits during the session.
- 🔎 **Input Extraction Chain** – Automatically extracts structured data (transport, diet, etc.) from natural language input using a prompt-based chain.
- 🧩 **LangChain Agent** – Routes user queries to appropriate tools based on input.
- 🌐 **Streamlit UI** – A clean, responsive chatbot interface for user interaction.
- 🧪 **Notebook-compatible** – Also works in Jupyter Notebooks for interactive testing.

## 🛠️ Technologies Used
- **LangChain** – For agent logic, tool routing, and memory.
- **Azure OpenAI** – GPT-based language model for reasoning and extraction.
- **Streamlit** – Frontend interface for chatting with the agent.
- **Python** – Backend logic and tool implementations.

## 📦 Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/paridhi3/Carbon-Optimiser.git
cd Carbon-Optimiser
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Set Environment Variables
Create a .env file and add the following:
```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_END_POINT=
DEPLOYMENT_NAME=
MODEL_NAME=
API_VERSION=
```
### 4. Run the app
```
streamlit run app.py
```

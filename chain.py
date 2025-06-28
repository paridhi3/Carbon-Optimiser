from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

extraction_template = PromptTemplate.from_template("""
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
    prompt=extraction_template.partial(
        valid_transports=", ".join(EMISSION_FACTORS["transport"].keys()),
        valid_energies=", ".join(EMISSION_FACTORS["energy"].keys()),
        valid_diets=", ".join(EMISSION_FACTORS["diet"].keys())
    )
)

@tool
def carbon_calculator(
    transport: str = "walk",
    distance_km: float = 0.0,
    energy: str = "electricity_avg",
    energy_kwh: float = 0.0,
    diet: str = "vegetables",
    meals_per_week: int = 0
) -> str:
    if transport == "walk" and distance_km == 0.0:
        notes.append("No transport details provided, assumed walking.")
    if energy_kwh == 0.0:
        notes.append("No energy usage provided, assumed 0 kWh.")
    if meals_per_week == 0:
        notes.append("No diet frequency provided, assumed no meals.")

    transport_emission = EMISSION_FACTORS["transport"].get(transport, 0) * distance_km
    energy_emission = EMISSION_FACTORS["energy"].get(energy, 0) * energy_kwh
    diet_emission = EMISSION_FACTORS["diet"].get(diet, 0) * meals_per_week
    total_emission = transport_emission + energy_emission + diet_emission

    response = f"Estimated weekly carbon footprint: {total_emission:.2f} kg CO₂"

    return response

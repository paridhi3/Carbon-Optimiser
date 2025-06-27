@tool
def carbon_calculator(
    transport: str = "walk",
    distance_km: float = 0.0,
    energy: str = "electricity_avg",
    energy_kwh: float = 0.0,
    diet: str = "vegetables",
    meals_per_week: int = 0
) -> str:
    """
    Calculates estimated weekly carbon footprint based on transport, energy, and diet.
    If any input is missing, it defaults to low-emission values (e.g., walking, vegetables).
    """
    transport_emission = EMISSION_FACTORS["transport"].get(transport, 0) * distance_km
    energy_emission = EMISSION_FACTORS["energy"].get(energy, 0) * energy_kwh
    diet_emission = EMISSION_FACTORS["diet"].get(diet, 0) * meals_per_week
    total_emission = transport_emission + energy_emission + diet_emission

    response = f"Estimated weekly carbon footprint: {total_emission:.2f} kg CO₂"

    return response

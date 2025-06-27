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
    Calculates estimated weekly carbon footprint for provided transport, energy, and diet values.
    Supports partial input — estimates only what it can based on available data.
    """
    response = []
    total_emission = 0.0

    if transport != "walk" or distance_km > 0:
        transport_emission = EMISSION_FACTORS["transport"].get(transport, 0) * distance_km
        total_emission += transport_emission
        response.append(f"Transport: {transport_emission:.2f} kg CO₂")

    if energy_kwh > 0:
        energy_emission = EMISSION_FACTORS["energy"].get(energy, 0) * energy_kwh
        total_emission += energy_emission
        response.append(f"Energy: {energy_emission:.2f} kg CO₂")

    if meals_per_week > 0:
        diet_emission = EMISSION_FACTORS["diet"].get(diet, 0) * meals_per_week
        total_emission += diet_emission
        response.append(f"Diet: {diet_emission:.2f} kg CO₂")

    response.append(f"**Total Estimated Weekly Carbon Footprint: {total_emission:.2f} kg CO₂**")
    return "\n".join(response)

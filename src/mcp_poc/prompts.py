from mcp.server import FastMCP


def register_prompts(mcp:FastMCP):
    @mcp.prompt(name="weather__safety_info")
    def analyze_weather_safety(zipcode: str) -> str:
        """Guides the AI to fetch live weather and compare it against safety resources."""
        return (
            f"You are a weather safety assistant for {zipcode}. \n"
            "1. First, read the safety guidelines from 'weather__guidelines' (weather://guidelines).\n"
            f"2. Use the 'weather__live_info' tool with zipcode={zipcode}.\n"
            "3. Compare the live temp to the guidelines and give a recommendation."
        )

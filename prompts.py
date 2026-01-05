from mcp.server import FastMCP


def register_prompts(mcp:FastMCP):
    @mcp.prompt(name="tf.weather.safety")
    def analyze_safety(zipcode: str) -> str:
        """Guides the AI to fetch live weather and compare it against safety resources."""
        return (
            f"You are a weather safety assistant for {zipcode}. "
            "1. First, read the safety guidelines from 'weather://guidelines'.\n"
            f"2. Use the 'get_live_weather' tool with zipcode={zipcode}.\n"
            "3. Compare the live temp to the guidelines and give a recommendation."
        )

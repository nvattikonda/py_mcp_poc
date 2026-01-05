from typing import Any

from mcp.server.fastmcp import FastMCP, Context

from weather import make_nws_request, format_alert, get_forecast, get_alerts

# Initialize FastMCP server
mcp = FastMCP("mcp_quickstart_server", instructions="server demos different capabilities of mcp", port=8000,
              host="0.0.0.0", streamable_http_path="/mcp", stateless_http=True,
              json_response=False)


@mcp.tool(name="tf.weather.alerts", description="provides weather alerts for a Two-letter US state code (e.g. CA, NY)")
async def get_weather_alerts(state: str) -> str:
    """provides weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)

    Returns:
        A alerts (str) for the given state code (e.g. CA, NY)
    """
    weather_alerts = await get_alerts(state)
    return weather_alerts


@mcp.tool(name="tf.weather.forecast",
          description="provides five-day weather forecast for five-digit zipcode of location in US")
async def get_weather_forecast(zipcode: str) -> str:
    """provides five-day weather forecast for five-digit zipcode of location in US.

    Args:
        zipcode: five-digit zipcode of location in US

    Returns:
        Five day forecast (str) for the given zipcode location in US
    """
    weather_forecast = await get_forecast(zipcode)
    return weather_forecast


@mcp.tool(name="tf.live.weather", description="provides live weather for five-digit zipcode of location in US")
async def get_live_weather(zipcode: str) -> str:
    """provides live weather for five-digit zipcode of location in US.

    Args:
        zipcode: five-digit zipcode of location in US

    Returns:
        live weather (str) for the given zipcode location in US
    """
    weather_forecast = await get_forecast(zipcode, time_periods=1)
    return weather_forecast


@mcp.tool(name="tf.server.info", description="provides information about the current server")
def server_info(ctx: Context) -> dict:
    """provide information about the current server."""
    return {
        "name": ctx.fastmcp.name,
        "instructions": ctx.fastmcp.instructions,
        "debug_mode": ctx.fastmcp.settings.debug,
        "log_level": ctx.fastmcp.settings.log_level,
        "host": ctx.fastmcp.settings.host,
        "port": ctx.fastmcp.settings.port,
    }


# Static context providing safety guidelines for different conditions
@mcp.resource(uri="weather://guidelines", name="tf.weather.guidelines",
              description="Provides safety guidelines for different weather conditions",mime_type="text/plain")
def get_weather_guidelines() -> str:
    """Provides safety guidelines for different weather conditions."""
    return (
        "Safe: < 90°F. Caution: 90-100°F (Heat Advisory). "
        "Danger: > 100°F (Excessive Heat Warning)."
    )


@mcp.prompt(name="tf.weather.safety", description="provides safety guidelines for different weather conditions")
def analyze_safety(zipcode: str) -> str:
    """Guides the AI to fetch live weather and compare it against safety resources."""
    return (
        f"You are a weather safety assistant for {zipcode}. "
        "1. First, read the safety guidelines from 'weather://guidelines'.\n"
        f"2. Use the 'get_live_weather' tool with zipcode={zipcode}.\n"
        "3. Compare the live temp to the guidelines and give a safety recommendation."
    )


def main():
    # Initialize and run the server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()

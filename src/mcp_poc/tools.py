from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from .weather import get_forecast, get_alerts

def register_tools(mcp:FastMCP):
    @mcp.tool(name="tf.weather.alerts")
    async def get_weather_alerts(state: str) -> str:
        """provides weather alerts for a Two-letter US state code (e.g. CA, NY)"""
        return await get_alerts(state)

    @mcp.tool(name="tf.weather.forecast")
    async def get_weather_forecast(zipcode: str) -> str:
        """provides five-day weather forecast for five-digit zipcode"""
        return await get_forecast(zipcode)

    @mcp.tool(name="tf.live.weather")
    async def get_live_weather(zipcode: str) -> str:
        """provides live weather for five-digit zipcode"""
        return await get_forecast(zipcode, time_periods=1)

    @mcp.tool(name="tf.server.info")
    def server_info(ctx: Context) -> dict:
        """provide information about the current server."""
        return {
            "name": ctx.fastmcp.name,
            "host": ctx.fastmcp.settings.host,
            "port": ctx.fastmcp.settings.port,
        }

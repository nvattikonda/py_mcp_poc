from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from .weather import get_forecast, get_alerts


def register_tools(mcp: FastMCP):
    @mcp.tool(name="weather__alerts")
    async def weather_alerts(state: str) -> str:
        """provides weather alerts for a Two-letter US state code (e.g. CA, NY)"""
        return await get_alerts(state)

    @mcp.tool(name="weather__forecast")
    async def weather_forecast(zipcode: str) -> str:
        """provides five-day weather forecast for provided five-digit zipcode"""
        return await get_forecast(zipcode)

    @mcp.tool(name="weather__live_info")
    async def live_weather(zipcode: str) -> str:
        """provides live weather for provided five-digit zipcode"""
        return await get_forecast(zipcode, time_periods=1)

    @mcp.tool(name="weather__server_info")
    def server_info(ctx: Context) -> dict:
        """
            Returns technical metadata about the weather server (name, host, port, negotiated protocol version and request payload).
        """
        return {
            "name": ctx.fastmcp.name,
            "host": ctx.fastmcp.settings.host,
            "port": ctx.fastmcp.settings.port,
            "mcp_protocol_version": ctx.request_context.request.__getattribute__("headers")["mcp-protocol-version"],
            "request_payload": ctx.request_context.request.__getattribute__("_body")
        }

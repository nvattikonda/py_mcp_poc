from mcp.server import FastMCP


def register_resources(mcp:FastMCP):
    @mcp.resource(uri="weather://guidelines", name="weather__guidelines")
    def weather_guidelines() -> str:
        """Provides safety guidelines for different weather conditions."""
        return (
            "Safe: < 90°F. Caution: 90-100°F (Heat Advisory). "
            "Danger: > 100°F (Excessive Heat Warning)."
        )

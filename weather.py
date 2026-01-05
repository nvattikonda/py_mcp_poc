from typing import Any

import httpx

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
GEO_CODING_API = "https://geocoding-api.open-meteo.com/v1/search"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"Unable to fetch alerts or no alerts found for this state:{state}."

    if not data["features"]:
        return f"No active alerts for this state:{state}."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


async def get_latitude_longitude(zipcode: str) -> tuple[int, Any, Any]:
    """Get latitude and longitude for a zipcode."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    query_params = {
        "name": zipcode,
        "countryCode": "US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=GEO_CODING_API, headers=headers, params=query_params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return response.status_code, data['results'][0]["latitude"], data['results'][0]["longitude"]
        except Exception:
            return response.status_code, None, None


async def get_forecast(zipcode: str) -> str:
    """Get weather forecast for a zipcode."""

    status_code, latitude, longitude = await get_latitude_longitude(zipcode)

    if status_code != 200:
        return f"Unable to fetch weather forecast for zipcode:{zipcode}"

    # Round to 4 decimal places to prevent the 'AdjustPointPrecision' redirect
    rounded_lat = round(latitude, 4)
    rounded_lon = round(longitude, 4)

    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{rounded_lat},{rounded_lon}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return f"Unable to fetch forecast data for this zipcode:{zipcode} with latitude:{rounded_lat} and longitude:{rounded_lon}location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

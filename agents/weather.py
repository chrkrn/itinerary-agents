import requests
import logging
logger = logging.getLogger(__name__)

def get_weather(state) -> str:
    """
    Gets the latitude and the longitude of a city in the world and calls an api to get the current temperature
    """
    logger.info(f"Getting weather for {state.get('city_or_town')}")

    #build query to open meteo endpoint
    lat = state.get('latitude')
    long = state.get('longitude')

    resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m").json()
    summary = f"The current temperature in {state.get('city_or_town')} is {resp["current"]["temperature_2m"]}{resp["current_units"]["temperature_2m"]}"

    logger.info(f"Weather summary for {state.get('city_or_town')}: {summary}")

    return {
        "weather_summary": summary
    }

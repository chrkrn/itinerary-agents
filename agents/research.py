import requests
import json
from agents.openrouter import chat_completion
import os

import logging
logger = logging.getLogger(__name__)

def llm_coordinates(state):
    """
    Use the current state to pull destination details and generate coordinates 
    """
    logger.info(f"Getting coordinates for {state.get('city_or_town')}")
    
    prompt = (
        "Return longitude and latitude for this location as JSON only with keys"
        f'"latitude" and "longitude": {state.get("city_or_town")}'
    )

    #call chat completions
    response_json = chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a geolocation assistant, only output JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    content = json.loads(response_json["choices"][0]["message"]["content"])

    logger.info(content)

    return {
        "longitude": float(content["longitude"]),
        "latitude": float(content["latitude"])
    }


def get_research_results(state):
    """
    Get search results for a given search term
    """

    logging.info("Calling Jina endpoint with search term: " + state.get("name"))

    j_api_key = os.getenv("JINA_KEY")

    resp = requests.get(url=f"https://s.jina.ai/{state.get('name')}",
    headers={
        "Authorization": f"Bearer {j_api_key}"
    }).text

    prompt = (
        f"Read the context and return the name, address, city_or_town, opening_times, indoor_or_outdoor, recommendations, and location_type of the business {state.get('name')} as JSON with only the pre mentioned keys"
        "location_type can be one of the following: resturant, cafe, museum, live venue, activity, park"
        "opening_times must be in the format: {'Monday': ['9am-12pm', '3pm-6pm'], 'Tuesday': 'Closed'}. If the location is open 24 hours use this format {'Monday': ['12-am-12pm']}"
        "indoor_or_outdoor can be one of three values: indoor, outdoor or indoor_and_outdoor. If the place is completely in a building, choose indoor. If the place is outside (e.g. a food market, a food stall, a park), choose outdoor. If a place has both indoor and outdoor public facilities, choose indoor_and_outdoor"
        "recommendations can be up to 3 sentences, referring to any popular thing to do at the location, e.g. any specialties that a resturant or cafe do, a certain spot in a park for a nice view or the best value class in art college. Only use the provided context, and if nothing shows up, answer with 'None'"
        f'"name", "address", "city_or_town", "location_type", "opening_times", "recommendations: {resp}'
    )

    response_json = chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a business research assistant, only output JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    content = json.loads(response_json["choices"][0]["message"]["content"])

    logger.info(f"Research results for {state.get('name')}: {content}")

    return {
        "name": str(content["name"]),
        "address": str(content["address"]),
        "opening_times": list(content["opening_times"]),
        "city_or_town": str(content["city_or_town"]),
        "location_type": str(content["location_type"]),
        "indoor_or_outdoor": str(content["indoor_or_outdoor"]),
        "recommendations": str(content["recommendations"]),
    }


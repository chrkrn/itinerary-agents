import requests
import json
import os
from langgraph.graph import START, END, StateGraph
from typing_extensions import NotRequired, TypedDict

from agents.research import llm_coordinates
from agents.weather import get_weather
from agents.vector_store import query_destination


def build_itinerary(state) -> str:

    query = f"Create an itinerary for {state.get("city_or_town")} for today"

    matches = query_destination(query, 3)

    if not matches:
        return "No destinations found in the DB yet."
    
    context = "\n".join(f"- {m['document']}" for m in matches)

    prompt = (
        f"Plan a day in {state.get('city_or_town')} and return an itinerary with no more than 3 places"
        f"Firstly look at the current weather details: {state.get('weather_summary')}"
        f"Firstly use the provided context to pick out 1-3 saved places in the location. Prioritise using locations that are close to each other (either within a mile or can travel to via public transport in 45 minutes), and opening times. If the itinerary has less than 3 places, fill in the blanks with your own suggestions"
        f"Each place JSON will summarise the time (ensure that the time given matches with opening times), location, address, saved_place (true if it was pulled from the context, otherwise false), and 3 recommendations on what to do (this can be based on the context). Return the itinerary as a JSON array with no other text. The JSON should be an array of objects, each object should have the following keys: time, location, address, saved_place, suggestion"
        f"In between each place JSON, provide a valid travel route with the time it will take to get there and the mode of transport (e.g. walk, public bus, public train, hire bike, taxi). For public transport, say what routes need to be taken. Return the travel suggestions as a JSON array with no other text. The JSON should be an array of objects, each object should have the following keys: from_location, to_location, travel_time, mode_of_transport"
        f"context: {context}"
    )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {or_api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(
            {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a travel planner, only output JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }   
        ),
        timeout=20
    )

    response.raise_for_status()

    print(response.json()["choices"][0]["message"]["content"])

    return {
        "itinerary": response.json()["choices"][0]["message"]["content"]
    }
     


class DestinationState(TypedDict):
    itinerary_query: str
    city_or_town: str
    weather_summary: str
    latitude: NotRequired[str]
    longitude: NotRequired[str]


class ItineraryPlanner():
    def __init__(self):
        workflow = StateGraph(DestinationState)
        workflow.add_node("llm_coordinates", llm_coordinates)
        workflow.add_node("get_weather", get_weather)
        workflow.add_node("build_itinerary", build_itinerary)

        workflow.add_edge(START, "llm_coordinates")
        workflow.add_edge("llm_coordinates", "get_weather")
        workflow.add_edge("get_weather", "build_itinerary")
        workflow.add_edge("build_itinerary", END)

        self.graph = workflow.compile()


    def invoke(self, city_or_town: str) -> DestinationState:
        return self.graph.invoke(
            {
                "city_or_town": city_or_town,
                "weather_summary": "",
                "latitude": 0.0,
                "longitude": 0.0
            }
        )


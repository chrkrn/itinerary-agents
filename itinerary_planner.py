import requests
import json
import os
from langgraph.graph import START, END, StateGraph
from typing_extensions import NotRequired, TypedDict

from agents.research import llm_coordinates
from agents.weather import get_weather
from agents.vector_store import query_destination
from agents.itinerary import build_itinerary


class DestinationState(TypedDict):
    """
    State for the destination information
    """
    city_or_town: str
    weather_summary: NotRequired[str]
    latitude: NotRequired[str]
    longitude: NotRequired[str]
    itinerary: NotRequired[dict]
    context: NotRequired[str]


class ItineraryPlanner():
    def __init__(self):
        """
        Set up the state graph for the itinerary planner
        Get Coordinates of location, get weather information of the area, then build an itinerary (pulling information from the vector store if anything relevant to the area has been saved)
        """

        #Nodes
        workflow = StateGraph(DestinationState)
        workflow.add_node("llm_coordinates", llm_coordinates)
        workflow.add_node("get_weather", get_weather)
        workflow.add_node("build_itinerary", build_itinerary)

        #Edges
        workflow.add_edge(START, "llm_coordinates")
        workflow.add_edge("llm_coordinates", "get_weather")
        workflow.add_edge("get_weather", "build_itinerary")
        workflow.add_edge("build_itinerary", END)

        self.graph = workflow.compile()


    def invoke(self, city_or_town: str) -> DestinationState:
        """Set up state and invoke graph using the user provided location"""
        return self.graph.invoke(
            {
                "city_or_town": city_or_town,
            }
        )


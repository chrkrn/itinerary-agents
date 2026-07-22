import requests
import json
import os
from langgraph.graph import START, END, StateGraph
from typing_extensions import NotRequired, TypedDict

from agents.weather import get_weather
from agents.research import get_research_results, llm_coordinates
from agents.vector_store import save_to_db


class SaveLocationState(TypedDict):
    """State for every location that is saved"""
    name: str
    address: str
    city_or_town: str
    location_type: str # e.g. cafe,resturant,activity
    opening_times: list 
    indoor_or_outdoor: str
    recommendations: NotRequired[str]
    latitude: NotRequired[str]
    longitude: NotRequired[str]


class SaveLocationForLater():
    def __init__(self):
        workflow = StateGraph(SaveLocationState)
        workflow.add_node("llm_coordinates", llm_coordinates)
        workflow.add_node("get_research_results", get_research_results)
        workflow.add_node("save_to_db", save_to_db)
       
        workflow.add_edge(START, "get_research_results")
        workflow.add_edge("get_research_results", "llm_coordinates")
        workflow.add_edge("llm_coordinates", "save_to_db")
        workflow.add_edge("save_to_db", END)

        self.graph = workflow.compile()


    def invoke(self, name: str) -> SaveLocationState:
        return self.graph.invoke(
            {
                "name": name,
                "address": "",
                "city_or_town": "",
                "location_type": "",
                "indoor_or_outdoor": "",
                "opening_times": [{"Monday": []},{"Tuesday": []},{"Wednesday": []},{"Thursday": []},{"Friday": []},{"Saturday": []},{"Sunday": []}],  
                "recommendations": "",
                "latitude": 0.0,
                "longitude": 0.0
            }
        )


from itineraryplanner import ItineraryPlanner
from save_places import SaveLocationForLater

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    """Return Welcome message"""
    return {"message": "Welcome to the Itinerary Planner API!"}


@app.get("/health")
def get_health():
    """Return health status of the API and model information"""
    return {
        "status": "healthy",
        "openrouter_model": os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
    }

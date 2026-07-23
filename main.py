from itinerary_planner import ItineraryPlanner
from save_places import SaveLocationForLater
import uvicorn
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])

app = FastAPI()

@app.get("/")
def get_root():
    """Return Welcome message"""
    return {"message": "Welcome to the Itinerary Planner API!"}

@app.get("/health")
def get_health():
    """Return health status of the API and other information can be added here"""
    return {
        "status": "healthy"
        }

@app.post("/request_itinerary")
def post_request_itinerary(location: str):
    """Generate an itinerary for a given city or town"""
    planner = ItineraryPlanner()

    logging.info(f"Generating itinerary for {location}")

    if not location:
        return {"error": "location parameter is required."}

    result = planner.invoke(location)
    return result

@app.post("/save_place")
def post_save_place(place: str):
    """Save a place for later"""
    saver = SaveLocationForLater()

    logging.info(f"Saving place: {place}")

    result = saver.invoke(place)
    return result


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

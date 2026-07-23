from agents.vector_store import query_destination
from agents.openrouter import chat_completion
import logging
logger = logging.getLogger(__name__)

def build_itinerary(state) -> str:
    """Build Itinerary with bias towards the vector db information"""

    # Query the Vector store to find saved places in the user provided area (top three matches)
    logger.info(f"Pulling context from vector store")

    query = f"Create an itinerary for {state.get("city_or_town")} for today"
    matches = query_destination(query, 3)

    if not matches:
        logger.info(f"No context generated from saved places")
        context = "No saved places found in the vector store for this location."
    else:
        logger.info(f"Context found from vector store")
        context = "\n".join(f"- {m['document']}" for m in matches)

    # Build the prompt for the LLM to generate an itinerary based on the current weather and any saved places in the vector store
    prompt = (
        f"Plan a day in {state.get('city_or_town')} and return an itinerary with no more than 3 places"
        f"Firstly look at the current weather details: {state.get('weather_summary')}"
        f"Firstly use the provided context to pick out 1-3 saved places in the location. Prioritise using locations that are close to each other (either within a mile or can travel to via public transport in 45 minutes), and opening times. If the itinerary has less than 3 places, fill in the blanks with your own suggestions"
        f"Each place JSON will summarise the time (ensure that the time given matches with opening times), location, address, saved_place (true if it was pulled from the context, otherwise false), and 3 recommendations on what to do (this can be based on the context). Return the itinerary as a JSON array with no other text. The JSON should be an array of objects, each object should have the following keys: time, location, address, saved_place, suggestion"
        f"In between each place JSON, provide a valid travel route with the time it will take to get there and the mode of transport (e.g. walk, public bus, public train, hire bike, taxi). For public transport, say what routes need to be taken. Each object should have the following keys: from_location, to_location, travel_time, mode_of_transport"
        f"context: {context}"
    )

    logger.info(f"Building itinerary for {state.get('city_or_town')}")

    #call chat completions with built prompts and context
    response_json = chat_completion(
        messages=[
                    {
                        "role": "system",
                        "content": "You are a travel planner, only output JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
    )

    it = response_json["choices"][0]["message"]["content"]
    logger.info(f"Itinerary generated: {it}")

    return {
        "itinerary": it
    }
     


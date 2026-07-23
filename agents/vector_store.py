import os
import chromadb
import time
import logging
logger = logging.getLogger(__name__)

DB_PATH = "./vector_store"
COLLECTION_NAME = "places"

def get_collection(collection_name):
    """Get Collection details from the local vector store"""
    logger.info(f"Getting collection: {collection_name} from vector store at {DB_PATH}")
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(name=collection_name)

def build_documents(state) -> str:
    """Turn state document into searchable natural language"""

    return(
        f"Name: {state.get('name', '')}, "
        f"Coordinates: {state.get('latitude')}, {state.get('longitude')}. "
        f"Address: {state.get('address', '')}, "
        f"City/Town: {state.get('city_or_town', '')}, "
        f"Location Type: {state.get('location_type', '')}, "
        f"Opening times: {state.get('opening_times', '')}, "
        f"Indoor or Outdoor: {state.get('opening_times', '')}, "
        f"Recommendations: {state.get('recommendations', '')}, "
    )


def save_to_db(state):
    """
    Save entry into a local vector db
    """

    #select collection
    collection = get_collection("places")

    #building document with the id
    record_id = f"{str(state.get("name")).replace(" ","_").lower()}_{str(state.get("city_or_town")).replace(" ","_").lower()}_{int(time.time() * 1000)}"
    document = build_documents(state)

    collection.add(ids=[record_id], documents=[document])
    logging.info(f"Saved record {record_id}")


def query_destination(query: str, n_results: int = 5):
    """Return stored information from db"""
    collection = get_collection("places")

    logger.info(f"Total Count of collection {collection_name}: {count}")

    count = collection.count()
    if count == 0:
        return []

    #query vector db
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count)
    )

    documents = results.get("documents", [[]])[0]

    return [
        {
            "document": doc
        }
        for doc in documents
    ]
    


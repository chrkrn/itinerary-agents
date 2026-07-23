# Itinerary Planner Project 

Personal project to learn more about Agentic AI approaches.

Itinerary planning agent with a bias on a saved list of places, aiming to
* Create an itinerary planner backed with LLMs, with options to save locations for later into a db.
* Must utilise free resources:
    * Application must be able to use free models and still respond reliably
    * Free Vector DB

## Requirements

For this project, OpenRouter is used to interface to AI models. Create a free account at https://openrouter.ai/, and create an API key. 
Note: This project has been tested with the `nvidia/nemotron-3-super-120b-a12b:free"` model, so an API key with no credits can be used to an extent (there is a daily limit should you want to run this project for free).

## Flow

User -> API -> Query -> Vector DB -> Response

## Features

TBC

## Local Setup

1. Create a local environment and install dependencies for the project via pip (TBC)

```
python -m venv venv
source venv/bin/activate  #venv\Scripts\activate in Windows
pip install -r requirements.txt
```

2. Create the .env file (using the .env.example template):

```
cp .env.example .env
```

Set the environment variables - these are the Jina api key (TBC), Openrouter API key and Openrouter Model to use (by default this will be set to `nvidia/nemotron-3-super-120b-a12b:free`)

```
JINA_KEY=your_jina_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free
```

3. Start the `main.py` script:
```
python main.py
```

The API will be avaialble on localhost:8000, with API documentation available on ```localhost:8000/docs```.

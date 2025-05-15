# tools.py
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_google_community import GooglePlacesTool

load_dotenv()
SERP_API_KEY = os.environ.get("SEARCH_API")
PLACES_API_KEY = os.environ.get("GPLACES_API_KEY")

@tool
def search(query: str):
    """Use SerpAPI to run a Google Search."""
    search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
    return search.run(query)

@tool
def places(query: str):
    """Use Google Places API to find a venue address."""
    formatted_query = query.replace("address", "").strip()
    return GooglePlacesTool().run(formatted_query)

def get_tools():
    return [search, places]
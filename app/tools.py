# tools.py
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_google_community import GooglePlacesTool

load_dotenv()
SERP_API_KEY = os.environ.get("SEARCH_API")
PLACES_API_KEY = os.environ.get("GPLACES_API_KEY")

# 환경변수의 유효성 확인
assert SERP_API_KEY, "SEARCH_API 키가 설정되지 않았습니다."
assert PLACES_API_KEY, "GPLACES_API_KEY 키가 설정되지 않았습니다."

@tool
def search(query: str):
    """Google에서 실시간 정보를 검색합니다. 지역/국가/도시 이름, 장소명, 발표 내용 등 일반 정보를 검색할 때 사용됩니다."""
    search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
    return search.run(query)

@tool
def places(query: str):
    """Google Places API를 사용하여 장소 주소를 검색합니다. 공연장 주소나 특정 장소 정보를 찾을 때 사용됩니다."""
    formatted_query = query.replace("address", "").strip()
    return GooglePlacesTool().run(formatted_query)

def get_tools():
    return [search, places]
# graph.py
from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import search_node, places_node, response_node, conditional_function_from_search_result, place_query_refiner_node, search_query_refiner_node
from app.agent.router import route_based_on_keyword

### 그래프 정의
# INFO: AgentState와 State의 차이
# 명확한 상태 필드(messages, search_result, places_result)가 있고 각 노드에 타입을 보장했을 때 AgentState가 유리
# 상태 필드가 명확하지 않은 경우 (간단한 테스트나 프로토타이핑)에는 State가 유리
graph = StateGraph(AgentState)

### 노드 추가
graph.add_node("search", search_node)
graph.add_node("places", places_node)
graph.add_node("respond", response_node)
graph.add_node("place_query_refiner", place_query_refiner_node)
graph.add_node("search_query_refiner", search_query_refiner_node)
graph.add_node("router", lambda state: {})  # 최소 형태의 "더미 노드"

### 진입점 설정
# 그래프가 실행될 때마다 작업을 시작할 위치
# INFO: add_edge(START, "node_name")와 set_entry_point("node_name")의 차이
# set_entry_point: 그래프 실행 시 가장 먼저 실행할 노드 지정, 실제 실행됨 => 단일 노드만 가능 (일반적인 에이전트 시작 시 사용)
# START: 그래프 상의 가상 시작 노드 (실제 실행은 X), 일반적으로 내부 경유 지점 또는 분기 포인트로 사용됨 => 여러 노드로 분기 가능 (복잡한 흐름 시 사용)
graph.set_entry_point("router")

### 조건부 엣지 설정
graph.add_conditional_edges(
    "router",
    route_based_on_keyword,    # search 또는 places 중 선택
    path_map={
        # "조건부 함수의 반환값": "노드 이름" >> 으로 구성
        "search_query_refiner": "search_query_refiner",
        "place_query_refiner": "place_query_refiner",
        "respond": "respond"
    }
)

# 검색 API 실행 후 장소 검색까지 하는지, 바로 답변하는지를 판단하는 조건부 엣지
graph.add_conditional_edges(
    "search",
    conditional_function_from_search_result,
    path_map={
        "place_query_refiner": "place_query_refiner",
        "respond": "respond"
    }
)

### 후속 처리
graph.add_edge("search_query_refiner", "search")
graph.add_edge("place_query_refiner", "places")
graph.add_edge("places", "respond")

### 끝지점 설정: 그래프 흐름의 종료를 나타냄
graph.add_edge("respond", END)

### 컴파일된 agent 반환
agent_excutor = graph.compile()

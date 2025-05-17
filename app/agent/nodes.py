# nodes.py
from app.tools import search, places
from langchain_core.messages import AIMessage
from app.agent.state import AgentState
from app.agent.model import llm

### 검색 노드 함수 정의
# 노드는 state["search_result"]로 상태를 읽고 새 값을 추가하면 이를 병합해서 상태를 이어감
def search_node(state):
    query = state["message"][-1].content

    # 도구 실행의 결과 저장
    result = search.run(query)
    return {
        # 멀티턴 대화를 위한 응답 저장
        # tools에서 나온 결과값은 에이전트의 최종 응답에 그대로 출력되면 안 되지만, 그래프의 내부 추론 흐름을 위한 context tracking 용도로 저장함
        "messages": [AIMessage(content=result)],
        "search_result": result
    }

### places 노드 함수 정의
def places_node(state):
    query = state["messages"[-1]]
    result = places.run(query)
    return {
        "messages": [AIMessage(content=result)],
        "places_result": result
    }

### response 노드 함수 정의
# REVIEW: 명시적으로 AgentState 타입을 지정한 이유? 코드 가독성 향상, 타입 검사 도구
def response_node(state: AgentState):
    # 검색 결과 선택
    context = state.get("places_result") or state.get("search_result") or "정보가 없습니다"
    query = state["messages"][-1].content

    # 응답 생성
    # TODO: 프롬프트 재작성 및 구조화된 출력으로 변경 (나중에 주소 형식 JSON으로 받아서 시각화)
    prompt = f"""사용자의 질문: {query}. \n
    다음 정보를 바탕으로 한국어로 응답을 생성하세요:\n\n{context}"""
    # TODO: streamlit에서 입력하도록 변경
    result = llm.invoke(prompt)

    return {
        "message": [AIMessage(content=result.content)]
    }

# INFO: user_input_node를 정의하지 않은 이유?
# 현재는 streamlit (또는 외부 입력)이 message를 직접 넘기기 때문에 사용자 입력 노드를 따로 둘 필요는 없다. (+ 간단한 구조이기 때문)
# 만약 사용자 입력을 상태에 추가하거나, 전처리(언어 감지, 욕설 필터 etc.)하는 등 기능을 추가한다면 필요에 따라 정의하면 됨

### conditional_function 정의
# LLM을 사용하여 사용자 쿼리의 의도를 분류한 후 검색 후 장소를 검색할지 말지 결정
def conditional_function_from_search_result(state):
    # 사용자 쿼리
    query = state["messages"[-1]].content
    search_result = state.get("search_result", "")

    # LLM에게 판단 요청 (few-shot prompting)
    # TODO: 이것도 확실히 한 단어로만 대답하도록 structured output parser 사용하기
    # TODO: prompt 파일로 분리
    prompt = f"""
당신은 질문을 분석해 장소 주소가 필요한 질문인지 아닌지를 판단하는 역할을 합니다.

예시:
Q: "테일러 스위프트가 마지막으로 공연한 장소는 어딘가요?"
A: places

Q: "테일러 스위프트가 최근에 발표한 앨범은 무엇인가요?"
A: respond

Q: "{query}"
검색 결과: "{search_result}"

위 질문은 어떤 분류에 해당하나요? ("places" 또는 "respond" 중 하나만 출력하세요.)
"""
    response  = llm.invoke(prompt)
    route = response.content.strip().lower()

    # 응답 결과 처리
    if route in {"places", "respond"}:
        return route
    return "respond"
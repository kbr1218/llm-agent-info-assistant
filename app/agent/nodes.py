# nodes.py
from app.tools import search, places
from langchain_core.messages import AIMessage, HumanMessage
from app.agent.state import AgentState
from langchain.prompts import ChatPromptTemplate
from app.agent.model import llm
from app.agent.conditional_edge import conditional_from_search_prompt, conditional_from_search_parser
from app.functions import load_template_from_yaml, get_last_user_query

response_template_with_context = load_template_from_yaml("prompt/respond_with_context.yaml")
response_template_without_context = load_template_from_yaml("prompt/respond_without_context.yaml")
refine_place_query_template = load_template_from_yaml("prompt/refine_place_query.yaml")
refine_search_query_template = load_template_from_yaml("prompt/refine_search_query.yaml")

response_prompt_with_context = ChatPromptTemplate.from_template(template=response_template_with_context)
response_prompt_without_context = ChatPromptTemplate.from_template(template=response_template_without_context)
refine_place_query_prompt = ChatPromptTemplate.from_template(template=refine_place_query_template)
refine_search_query_prompt = ChatPromptTemplate.from_template(template=refine_search_query_template)

### SerpAPI를 위한 검색어 전처리 노드
def search_query_refiner_node(state):
    query = get_last_user_query(state["messages"])
    history = "\n".join(
        m.content for m in state["messages"]
        if isinstance(m, HumanMessage) and m.content != query
    )

    prompt = refine_search_query_prompt.format(
        query=query,
        history=history
    )
    refined_query = llm.invoke(prompt).content.strip()

    return {
        "messages": [AIMessage(content=f"[검색용 보정 쿼리]\n{refined_query}")],
        "refined_place_query": refined_query
    }

### 검색 노드 함수 정의
# 노드는 state["search_result"]로 상태를 읽고 새 값을 추가하면 이를 병합해서 상태를 이어감
def search_node(state):
    query = state.get("refined_search_query", state["messages"][-1].content)

    # 도구 실행의 결과 저장
    result = search.run(query)
    return {
        # 멀티턴 대화를 위한 응답 저장
        # tools에서 나온 결과값은 에이전트의 최종 응답에 그대로 출력되면 안 되지만, 그래프의 내부 추론 흐름을 위한 context tracking 용도로 저장함
        "messages": [AIMessage(content=result)],
        "search_result": result
    }

### Google Places API를 위한 검색어 전처리 노드
def place_query_refiner_node(state):
    query = get_last_user_query(state["messages"])
    search_result = state.get("search_result", "")      # search 경로가 아닐 경우 빈 문자열
    history = "\n".join(
        m.content for m in state["messages"]
        if isinstance(m, HumanMessage) and m.content != query
    )
    prompt = refine_place_query_prompt.format(
        query=query,
        history=history,
        search_result=search_result
        )
    refined_query = llm.invoke(prompt).content.strip()

    return {
        "messages": [AIMessage(content=f"[장소 검색용 보정 쿼리]\n{refined_query}")],
        "refined_place_query": refined_query
    }

### places 노드 함수 정의
def places_node(state):
    query = state.get("refined_place_query", state["messages"][-1].content)
    result = places.run(query)
    return {
        "messages": [AIMessage(content=result)],
        "places_result": result
    }

### response 노드 함수 정의
# REVIEW: 명시적으로 AgentState 타입을 지정한 이유? 코드 가독성 향상, 타입 검사 도구
def response_node(state: AgentState):
    # 검색/주소 결과
    search_result = state.get("search_result", "")
    places_result = state.get("places_result", "")
    
    query = get_last_user_query(state["messages"])
    # 대화 이력
    history = "\n".join(
        m.content for m in state["messages"]
        if isinstance(m, HumanMessage) and m.content != query
    )

    # context 구성: 정보 + 맥락 포함
    context = ""
    if places_result:
        context += f"[주소 검색 결과]\n{places_result}\n"
    if search_result:
        context += f"[검색 결과 요약]\n{search_result}\n"

    # 최종 응답을 생성하기 위한 프롬프트
    if context:
        prompt = response_prompt_with_context.format(
            query=query,
            context=context,
            history=history)
    else:
        prompt = response_prompt_without_context.format(
            query=query,
            history=history)
    response = llm.invoke(prompt)

    return {
        "messages": [AIMessage(content=response.content)]
    }

# INFO: user_input_node를 정의하지 않은 이유?
# 현재는 streamlit (또는 외부 입력)이 message를 직접 넘기기 때문에 사용자 입력 노드를 따로 둘 필요는 없다. (+ 간단한 구조이기 때문)
# 만약 사용자 입력을 상태에 추가하거나, 전처리(언어 감지, 욕설 필터 etc.)하는 등 기능을 추가한다면 필요에 따라 정의하면 됨

### conditional_function 정의
# LLM을 사용하여 사용자 쿼리의 의도를 분류한 후 검색 후 장소를 검색할지 말지 결정
def conditional_function_from_search_result(state):
    messages = state["messages"]
    search_result = state.get("search_result", "")

    # 가장 최신 사용자 질문만 추출
    query = get_last_user_query(messages)

    # 가장 마지막 메시지 제외한 대화 이력
    history = "\n".join(m.content for m in messages[:-1])

    # formated prompt 생성 및 LLM 호출
    prompt = conditional_from_search_prompt.format(
        query=query,
        history = history,
        search_result=search_result,
        format_instructions = conditional_from_search_parser.get_format_instructions()
    )
    response  = llm.invoke(prompt)
    parsed = conditional_from_search_parser.parse(response.content)
    return parsed["route"]

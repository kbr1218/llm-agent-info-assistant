# router.py
from app.agent.model import llm

def route_based_on_keyword(state):
    query = state["messages"][-1].content
    # TODO: 얘도 프롬프트 디렉토리로 분리
    prompt = f"""
    아래 질문은 장소 정보를 찾는 의도가 있는 질문인가요?

    Q: "{query}"

    장소 관련 질문이면 "places", 아니면 "search"라고만 답하세요.
    """

    response = llm.invoke(prompt)
    return response.content.strip().lower()

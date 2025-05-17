# state.py
from typing import TypedDict, Optional, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 메시지 정의 (list type이며 add_messages 함수를 사용하여 메시지 추가)
    messages: Annotated[list, add_messages]
    # search와 place 노드에서 처리한 결괏값을 state에 저장하기 위해 정의
    # Optional: 각각의 state는 문자열일 수도 있고, 없을 수도(None) 있다는 의미
    search_result: Optional[str]
    places_result: Optional[str]

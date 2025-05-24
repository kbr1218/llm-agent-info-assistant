# functions.py
import yaml
from langchain_core.messages import HumanMessage, AIMessage

# .yaml 형식의 프롬프트 불러오기
def load_template_from_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data['template']

# 대화 기록에서 사용자의 쿼리 찾기
def get_last_user_query(messages):
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""

# say_hi_to_user를 제외한 대화 이력을 가져오는 함수
def get_filtered_history(messages, exclude_intro: str = None, exclude_query: str = None):
    if exclude_intro is None:
        exclude_intro = load_template_from_yaml("prompt/say_hi_to_user.yaml")

    return "\n".join(
        m.content
        for m in messages
        if isinstance(m, (HumanMessage, AIMessage))
        and (exclude_intro.strip() not in m.content if exclude_intro else True)
        and (exclude_query is None or m.content != exclude_query)
    )
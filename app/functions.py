# functions.py
import yaml
from langchain_core.messages import HumanMessage

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
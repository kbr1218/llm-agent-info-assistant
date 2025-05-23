# conditional_edge.py
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from app.functions import load_template_from_yaml 

# 구조화된 응답 스키마 정의 (places || respond)
response_schemas = [
    ResponseSchema(
        name = "route",
        description='"place_query_refiner" 또는 "respond" 중 하나로만 응답하세요.'
    )
]
conditional_from_search_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 프롬프트 템플릿
conditional_from_search_template = load_template_from_yaml("prompt/conditional_from_search.yaml")
conditional_from_search_prompt = ChatPromptTemplate.from_template(conditional_from_search_template)

# router.py
from app.agent.model import llm
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from app.functions import load_template_from_yaml 

# 구조화된 응답 정의
response_schemas = [
    ResponseSchema(
        name="route",
        description='"search", "place_query_refiner", "respond" 중 하나로만 응답하세요.'
    )
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 프롬프트 템플릿
router_template = load_template_from_yaml("prompt/router.yaml")
router_prompt = ChatPromptTemplate.from_template(router_template)

def route_based_on_keyword(state):
    query = state["messages"][-1].content
    prompt = router_prompt.format(
        query=query,
        format_instruction= parser.get_format_instructions()
    )
    response = llm.invoke(prompt)
    parsed = parser.parse(response.content)
    return parsed["route"]

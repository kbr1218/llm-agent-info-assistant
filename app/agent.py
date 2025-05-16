# agent.py
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from app.model import get_model
from app.tools import get_tools

model = get_model()
tools = get_tools()
agent = create_react_agent(model, tools)

# def run_agent_stream(user_input: str):
#     messages = [HumanMessage(content=user_input)]

#     def stream_generator():
#         for step in agent.stream({"messages": messages}, stream_mode="values"):
#             message = step["messages"][-1]
#             chunk = message[1] if isinstance(message, tuple) else message.content
#             yield chunk
    
#     return stream_generator


# stream 방식 적용하지 않은 응답
def run_agent_stream(user_input):
    full_message = ""
    input_dict = {"messages": [("human", user_input)]}
    print(f"-------input dict: {input_dict}")

    for step in agent.stream(input_dict, stream_mode="values"):
        message = step["messages"][-1]
        print(f"-------message: {message}")
        chunk = message[1] if isinstance(message, tuple) else message.content
        # full_response += chunk
        final_message = chunk
        print(f"--------final_message: {final_message}")

    return final_message
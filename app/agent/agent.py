# # agent.py
# from langchain_core.messages import HumanMessage, AIMessage
# from langgraph.prebuilt import create_react_agent
# from app.agent.model import get_model
# from app.tools import get_tools

# model = get_model()
# tools = get_tools()
# agent = create_react_agent(model, tools)

# # stream 방식 적용하지 않은 응답
# def run_agent_stream(user_input, history=[]):
#     input_messages = history + [HumanMessage(content=user_input)]
#     input_dict = {"messages": input_messages}

#     final_message = ""
#     for step in agent.stream(input_dict, stream_mode="values"):
#         message = step["messages"][-1]
#         chunk = message[1] if isinstance(message, tuple) else message.content
#         final_message = chunk
#         print(f"--------final_message: {final_message}")

#     return final_message
# agent_prompt.py
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
Answer the following question step-by-step.
Use tools if needed, but only return the FINAL answer at the end.
Return only the final summarized answer as your output IN KOREAN.

Question: {input}
""")
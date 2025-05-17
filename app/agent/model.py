# model.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API")

### LLM 정의
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key=GEMINI_API_KEY,
                             model_kwargs={"stream": True})

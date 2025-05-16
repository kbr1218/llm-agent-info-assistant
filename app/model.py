# model.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API")

def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                                                      google_api_key=GEMINI_API_KEY,
                                                                      stream=True)
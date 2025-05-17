# main.py
from app.ui import run_app
from langchain_teddynote import logging

logging.langsmith("agent-assistant")

if __name__ == "__main__":
    run_app() 
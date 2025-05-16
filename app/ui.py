# ui.py
import streamlit as st
from app.agent import run_agent_stream
from prompt.say_hi_to_user import say_hi
from langchain_core.messages import HumanMessage, AIMessage

# 페이지 기본 설정
st.set_page_config(page_title="A.M.A.", page_icon="👨🏻‍🎓", layout="wide")

def run_app():
    st.title("실시간 정보 검색 및 장소 탐색을 위한 AI Agent🐱‍🏍")
    st.caption("Github repo: https://github.com/kbr1218/llm-agent-info-assistant")
    st.divider()
    st.balloons()

    # 사이드바 추가
    with st.sidebar:
        st.header("🧹 옵션")
        if st.button("💬 채팅 기록 초기화", type="primary", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "assistant", "content": say_hi}
            ]
            st.success("✔ 채팅 기록이 초기화되었습니다.")

    # 채팅 기록이 없다면 첫 번째 소개 메시지 출력
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": say_hi}
        ]

    # 메시지 입력
    user_input = st.chat_input(placeholder="질문을 입력하세요. ", max_chars=150)

    col1, col2 = st.columns([1, 1])
    with col1:
        # chat history 출력
        for message in st.session_state.chat_history:
            avatar = "👩🏻‍🦰" if message['role'] == "user" else "👨🏻‍🎓"
            with st.chat_message(message['role'], avatar=avatar):
                st.markdown(message['content'])

        # 사용자 입력
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="👩🏻‍🦰"):
                st.markdown(user_input)

            # 대화 기록 변환
            history = []
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    history.append(AIMessage(content=msg["content"]))

            with st.spinner("Agent가 응답을 생성하는 중..."):
                assistant_response = run_agent_stream(user_input, history[:-1])  # 마지막 user는 run_agent_stream 안에서 추가됨

            # Agent의 응답 출력 및 chat history에 저장
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            with st.chat_message("assistant", avatar="👨🏻‍🎓"):
                st.markdown(assistant_response)
# ui.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from app.agent.graph import agent_excutor
from app.agent.state import AgentState
from app.functions import load_template_from_yaml

load_dotenv()
GPLACES_API_KEY = os.environ.get("GPLACES_API_KEY")

say_hi = load_template_from_yaml("prompt/say_hi_to_user.yaml")

def run_app():
    # 페이지 기본 설정
    st.set_page_config(page_title="building an agent,, for reasons", page_icon="👾", layout="wide")

    # 페이지 레이아웃 설정
    st.title("LangGraph 기반 정보 탐색 & 장소 조회 에이전트🐱‍🏍")
    st.caption("🔗 Github repo (still working on it,,): https://github.com/kbr1218/llm-agent-info-assistant")
    st.divider()
    # st.balloons()

    # 사이드바 추가
    with st.sidebar:
        st.header("🧹 옵션")
        if st.button("💬 채팅 기록 초기화", type="primary", use_container_width=True):
            st.session_state.chat_history = [{"role": "assistant", "content": say_hi}]
            st.success("✔ 채팅 기록이 초기화되었습니다.")

    # 채팅 기록이 없다면 첫 번째 소개 메시지 출력
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": say_hi}]

    # 메시지 입력
    user_input = st.chat_input(placeholder="질문을 입력하세요. ", max_chars=150)

    col1, col2 = st.columns([2, 1])
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
                
            # LangGraph 실행을 위한 상태 메시지 준비
            history: List[HumanMessage | AIMessage] = []
            for msg in st.session_state.chat_history[:-1]:
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    history.append(AIMessage(content=msg["content"]))
                
            messages = history + [HumanMessage(content=user_input)]

            # LangGraph Agent 실행
            with st.spinner("Agent가 응답을 생성하는 중..."):
                output: AgentState = agent_excutor.invoke({
                    "messages": messages,
                    "search_result": None,
                    "places_result": None
                })
                
            assistant_message = output["messages"][-1].content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})

            # Agent의 응답 출력 및 chat history에 저장
            with st.chat_message("assistant", avatar="👨🏻‍🎓"):
                st.markdown(assistant_message)

    with col2:
        st.subheader("🗺️ 지도 보기")

        if user_input:
            st.text("✅ user_input 있음")

            st.write("🔎 raw LLM response:", output)

            if "map_place_id" in output:
                st.text("✅ map_place_id 키 존재")
            if output.get("embed_location"):
                st.text("✅ embed_location 값 존재")

            if "map_place_id" in output and output["map_place_id"]:
                embed_url = f"https://www.google.com/maps/embed/v1/place?key={GPLACES_API_KEY}&place_id={output['map_place_id']}"

                st.text("🔍 Google Maps Embed URL:")
                st.code(embed_url)

                st.components.v1.html(
                    f"""<iframe width="100%" height="300" frameborder="0" style="border:0"
                    referrerpolicy="no-referrer-when-downgrade" src="{embed_url}" allowfullscreen></iframe>""",
                    height=310
                )
            else:
                st.markdown("현재 표시할 장소가 없습니다.")
# 🐱‍🏍 실시간 정보 검색 및 장소 탐색을 위한 AI Agent
실시간 정보 검색과 장소 탐색을 도와주는 LangGraph 기반 멀티턴 대화형 AI 에이전트입니다.  

사용자의 자연어 질문을 분석하여 **웹 검색, 장소 검색, 자연어 응답 생성, 지도 임베딩**까지 한 번에 수행합니다. 

<br>

## 📌 주요 기능
1. 실시간 웹 정보 검색 (SerpAPI)
    - 뉴스, 인물, 발표 정보 등 실시간 정보 검색
    - 검색 쿼리 보정 기능으로 **검색 실패 시 재검색 자동 시도** (3번까지!)
      
2. 장소 기반 검색 (Google Places API)
    - 공연장, 미술관, 식당 등 장소 이름 추출 후 주소 검색
    - 지도 임베딩을 통한 시각적 응답 제공
      
3. LLM 기반 자연어 응답
    - LangChain + Gemini 기반 응답 생성
    - 검색결과/주소 정보를 맥락으로 응답 문장 구성
      
4. LangGraph 기반 멀티턴(Multi-turn) 흐름 제어
    - 쿼리 분류 → 검색 → 장소 탐색 → 응답 생성 흐름을 그래프로 구성
    - 조건부 엣지(Conditional Edge)로 자연스러운 대화 흐름 구현

<br>

## ⚙️ 기술 스택
| 분류     | 기술                                                            |
| --------- | ------------------------------------------------------------- |
| 프레임워크     | LangGraph + LangChain  |
| LLM       | Google Gemini (gemini-2.0-flash) via `langchain-google-genai` |
| 검색 API    | SerpAPI                                                       |
| 장소 탐색 API | Google Places API (`langchain_community`)                     |
| 프롬프트    | LangChain PromptTemplate, YAML 기반 템플릿 관리   |
| UI     | Streamlit                                                     |
| 빌드 및 패키지 관리   | Poetry                                         |


<br>

## 🛸 그래프 구조
![graph](https://github.com/kbr1218/llm-agent-info-assistant/blob/47c8f4e835bdbfdc40413a82ddcfd30144c13ae1/img/output4.png)

- 그래프 기반 워크플로우 (LangGraph) 사용
- 조건부 분기: `route_based_on_keyword`, `conditional_function_from_search_result`, `requery_router`
- LLM 출력 구조화: `StructuredOutputParser`, JSON 응답 파싱

<br>

## 🖥️ 실행 화면 및 예시
#### 예시 1: 정보 검색
- 사용자 입력 >> SerpAPI 검색 >> 응답
- (여기 사진 추가)

#### 예시 2: 장소 검색 + 지도 표시
- 사용자 입력 >> Google Places API 장소 검색 >> 응답
- (여기 사진 추가)

#### 예시 3: 정보 검색 + 장소 검색 + 지도 표시
- 사용자 입력 >> SerpAPI 검색 >> Google Places API 장소 검색 >> 응답
- (여기 사진 추가)

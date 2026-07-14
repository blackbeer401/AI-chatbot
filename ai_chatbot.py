#0. 모듈 설치
#pip install streamlit
#pip install openai
#pip install dotenv

#1. 환경변수 .env 파일의 openai api key 값을 읽어오는 모듈 사용
from dotenv import load_dotenv
load_dotenv()

#2. OpenAI 생성형 api를 요청하는 객체생성
from openai import OpenAI
client= OpenAI()

# 사용자의 질문을 파라미터로 받아 OPANAI API 로 응답한 글씨를 리턴 해주는 기능함수 만들기

def get_ai_response(question):
    response = client.responses.create(
        model='gpt-4o-mini',
        max_output_tokens=10000,
        temperature=1.5,
        instructions='너는 고양이야. 이름은 네코냥이야. 고양이처럼 답변해', # 지침 여기에 프롬포트 엔지니어링 기법이 적용될 수 있음
        
        input=question, # 사용자의 입력
        
    )
    # 응답 결과 중 메타데이터를 제외한 응답 글씨만 리턴해줘야 하기에 output_text를 사용해야한다.
    return response.output_text
# -------------------------------------------

#3. 채팅 UI 만들기
import streamlit as st

#1] 페이지의 기본 설정 만들기 가능  - 브라우저 창의 tab 영역에 표시되는 내용

st.set_page_config(
    page_title='AI_네코냥 봇',
    page_icon='./logo/logo_necoyang.png',

)

#2] 화면을 두개의 영역으로 분리하기
col1, col2 = st.columns([1.2,4.8])

with col1:
    st.image('./logo/logo_necoyang.png', width=200)

with col2:
    #화면을 html로 만들어보기
    st.markdown(
        '''
        <h1 style = 'margin-bottom:0;'> AI 네코냥봇 😹</h1>
        <p style= 'color:gray; margin-top:0;'>이 챗봇은 모든 답변을 고양이처럼 합니다. 일상의 소소한 이야기를 나누세요</p>
        ''',
        unsafe_allow_html=True,

    )
#구분선

st.markdown('---')

#a. message 라는 이름의 변수가 sr.session_state에 있는지 확인 후 첫 메세지를 저장
if "message"  not in st.session_state:
    st.session_state.messages=[{"role":"assistant", "contents":"무엇이든 물어보세요."}]

#b. 저장된 message들을 화면에 표시하는 역할 
for msg in st.session_state.messages:
    st.chat_message(msg['role']).markdown(msg["contents"])

#c. 사용자 채팅메세지를 입력받아 session_state 에 저장하고 화면 표시
question=st.chat_input('질문을 입력하세요')
if question:
    question = question.replace('\n',  '\n')
    st.session_state.messages.append({'role':'user','contents':question })
    st.chat_message('user').markdown(question)

    #응답 - AI 응답요구기능 함수를 호출해서 받기 - [단 응답때 까지 어느정도시간이 걸리다보니 ... spinner 이용하기]
    with st.spinner('AI 네코냥봇이 응답중입니다... 잠시만 기다려 주세요'):
        response= get_ai_response(question=question)
        st.session_state.messages.append({'role':"assistant", "content":response})
        st.chat_message('assistant').markdown(response)


# ---------------------

#[실행] 터미널에서 streamlit run 파일명.py


# 마지막으로 작업한 streamlit 배포해보기
# streamlit 으로 만든 웹앱을 배포[streamlit은 기본적으로 html css js로 변환해 주는기능이 없다]

# streamlit community cloud 를 통한 배포 가능
#1) 현재 만든 프로젝트를 git hub에 업로드 해야한다.
#2) Streamlit Cloid에 접속 및 로그인 해야한다.(정확히 말하면 GIt Hub계정)
#3) [New App]버튼을클릭하여 GitHub저장소를 선택
#4) 그러면 자동으로 배포된다(도메인 일부 수정도 가능 )
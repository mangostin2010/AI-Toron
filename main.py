import openai
import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space 
import random

st.set_page_config(page_title="AI와 토론하다, AITORON", page_icon="💬")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

#TopicList = ['모든 기독교인은 교회에 꼭 가야하나요?', '착하게 살면 되지 왜 꼭 하나님을 믿어야 합니까?', '교회가서 헌금을 꼭 내야하나요?', '크리스찬도 문신을 해도 되나요?', '기독교에서 동성애에 대한 입장은 무엇인가요?', '기독교에서의 음주에 대한 입장은 어떻게 되나요?', '기독교인이 마술이나 요술에 대해 어떻게 생각해야 할까요?', '기독교인이 불륜 저지르면 어떻게 해야 할까요? 용서는 가능한가요?', '기독교인이 비디오, 컴퓨터 게임을 해도 되나요?','기독교인은 아이돌 노래와 같은 세상 노래를 들어도 되나요?','기독교인이 클럽에 다니는 것은 괜찮나요?','왜 하나님께서는 나쁜고 슬픈일이 일어나게 하십니까?','김주원은 정한나를 좋아하나?', '학교 규칙을 만들때 학생들이 참여해야하나?']
TopicList = ['시험은 필요할까?','학원은 다녀야 할까?','초등학생이 이성을 사귀어도 될까?','선의의 거짓말을 해도 될까?','초등학생에게 스마트폰이 필요할까?','초등학생이 게임을 해도 될까?','학교에 CCTV를 설치해야할까?','돈이 많아야 행복할까?','가난은 개인의 탓일까?','과정이 중요할까? 결과가 중요할까?','미래를 위해 현재를 희생해도 될까?','교복을 폐지해야 한다.','인터넷 실명제를 도입해야 한다.','자살은 개인의 선택으로서 존중받아야 한다.','인공지능은 인간을 완전히 대체할 수 있다.','게임 중독은 질병이다.','수술실 CCTV 설치를 의무화해야 한다.','인공지능 기술의 발전은 인간의 삶의 질 향상에 공헌한다.','인공지능의 창작물에도 저작권을 인정해 주어야 한다.','인터넷 상의 ‘악플’, 처벌해야 한다.','양성평등을 위해 여자도 군대에 보내야 한다.','유전자 조작 농산물의 생산 및 유통, 금지해야 한다.','심청이가 아버지를 위해 인당수에 몸을 던진 것은 효도이다.','홍길동이 부자의 재산을 빼앗아 가난한 사람들에게 나눠준 것은 옳은 일이다.']
# 세션 내에서 한 번만 주제 선택
if "session_topic" not in st.session_state:
    st.session_state.session_topic = random.choice(TopicList)

Topic = st.session_state.session_topic
st.header(':rainbow[AI와 토론하다, AITORON]', divider='rainbow')
st.subheader(Topic)

add_vertical_space(2)
#streamlit 세션관리
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

openai.api_base = 'https://api.chatanywhere.cn'
openai.api_key = "sk-ERbEZ6g35cYPM7DcMylctYXpg92zF60UaaVGMZWfPU1x7dpX"

systemrole = f"""
You are a person who is very good at discussioning something.
Follow this rule:
  1. You are to rebuttal user.
  2. Have a discussion about the following topic.
  3. You may speak other languages.
  4. Do not select the netural, REBUTTAL USER.
  5. Make every your answer be logical.
  6. Do not get out from the discussion topic; if user says the answer that is not related to the topic, say it and give your opinion.
  7. Make every your answer short.
  8. You are a Christian and you believe the Bible is True.
  9. If you have the same opinion with user, change your opinion opposite to user.
  10. Do not conclude the answer for the topic, just rebuttal user.
  Discussion Topic: {Topic}
  """

messages = [
    {"role": "system", "content": systemrole},
]

User_Message = st.chat_input("의견을 나누고 반박하세요!")


if User_Message:
  Chat_User = st.chat_message("user")

  if Chat_User.markdown(User_Message):
    item =  {"role": "user", "content": User_Message}
    messages.append(item)
    st.session_state.messages.append({"role": "user", "content": User_Message})

  with st.chat_message("assistant"):
      message_placeholder = st.empty()
      full_response = ""
      for response in openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages,
          stream=True,
      ):
          full_response += response.choices[0].delta.get("content", "")
          message_placeholder.markdown(full_response + "▌")
          time.sleep(0.1)
      message_placeholder.markdown(full_response)
      messages.append(full_response)
      st.session_state.messages.append({"role": "assistant", "content": full_response})

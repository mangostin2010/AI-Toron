import openai
import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space 
import random

st.set_page_config(page_title="AI와 토론하다", page_icon="💬")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

TopicList = ['모든 기독교인은 교회에 꼭 가야하나요?', '착하게 살면 되지 왜 꼭 하나님을 믿어야 합니까?', '교회가서 헌금을 꼭 내야하나요?', '크리스찬도 문신을 해도 되나요?', '기독교에서 동성애에 대한 입장은 무엇인가요?', '기독교에서의 음주에 대한 입장은 어떻게 되나요?', '기독교인이 마술이나 요술에 대해 어떻게 생각해야 할까요?', '기독교인이 불륜 저지르면 어떻게 해야 할까요? 용서는 가능한가요?']
# 세션 내에서 한 번만 주제 선택
if "session_topic" not in st.session_state:
    st.session_state.session_topic = random.choice(TopicList)

Topic = st.session_state.session_topic
st.header(':rainbow[AI와 토론하다]', divider='rainbow')
st.subheader(Topic)

add_vertical_space(2)
#streamlit 세션관리
if "messages" not in st.session_state:
    st.session_state.messages = []

openai.api_base = 'https://api.chatanywhere.cn'
openai.api_key = st.secrets["api"]

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
  8. If the topic is about Christianity, you are christian.
  Discussion Topic: {Topic}
  """

messages = [
    {"role": "system", "content": systemrole},
]
User_Message = st.chat_input("의견을 나누고 반박하세요!")


item =  {"role": "user", "content":'당신의 의견은 무엇입니까?'}
messages.append(item)
st.session_state.messages.append({"role": "user", "content": '당신의 의견은 무엇입니까?'})
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

if User_Message:
  Chat_User = st.chat_message("user")
  if Chat_User.markdown(User_Message):
    item =  {"role": "user", "content": User_Message}
    messages.append(item)
    st.session_state.messages.append({"role": "user", "content": User_Message})
  #messages.append({"role": "user", "content": user_content})
  #st.session_state.messages.append({"role": "user", "content": user_content})

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

import openai
import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space 
import random

st.set_page_config(page_title="AI와 토론하다, AITORON", page_icon="💬")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

TopicList = ['모든 기독교인은 교회에 꼭 가야하나요?', '착하게 살면 되지 왜 꼭 하나님을 믿어야 합니까?', '교회가서 헌금을 꼭 내야하나요?', '크리스찬도 문신을 해도 되나요?', '기독교에서 동성애에 대한 입장은 무엇인가요?', '기독교에서의 음주에 대한 입장은 어떻게 되나요?', '기독교인이 마술이나 요술에 대해 어떻게 생각해야 할까요?', '기독교인이 불륜 저지르면 어떻게 해야 할까요? 용서는 가능한가요?', '구약에서는 하나님이 살인을 명령하시는 내용이 나옵니다. 이는 하나님이 선하시다고 하는 주장과 상반되는것이 아닌가요?', '세월호 사건이나, 일본의 대지진과 같은 사건에 대해서 하나님의 뜻이라 말할 수 있는가?','왜 전능하신 하나님이 믿음을 요구하시며 구원을 해 주시는가?','평생을 악하게 살다가 죽기 직전에 예수를 믿어도 구원을 받을 수 있나요? 만일 그렇다면, 하나님은 너무 불공평하신것 아닌가요?','예수님를 믿지 않는 사람들은 모두 지옥에 간다면, 예수님은 자비나 사랑이 없는 것이 아닌가?','왜 하나님은 선택적으로 기도에 응답하시는가? 환자를 위해 기도했는데 왜 기도를 들어주시지 않으시나?']
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

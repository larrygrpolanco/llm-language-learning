from openai import OpenAI
import streamlit as st


openai_api_key = st.secrets["OPENAI_API_KEY"]

with st.sidebar:
    practice_langauge = st.text_input("Which language are you learning?", "Chinese")
    learner_level = st.select_slider("CEFR Level", ["A1", "A2", "B1", "B2", "C1", "C2"])
    conversation_context = st.text_area(
        "Do you have a specific context in mind?",
        placeholder="Ordering food at a resturant",
    )
    translation_on = st.toggle("Provide english tranlation?")


st.title("Conversation Dictionary")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

import streamlit as st

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

google_api_key = st.secrets["GOOGLE_API_KEY"]

st.title("Conversation Dictionary")

# Button to clear responses
if st.button("Clear All Responses"):
    st.session_state["responses"] = []  # Reset the list of responses

with st.sidebar:
    st.title("Language Settings")
    practice_language = st.text_input("Which language are you learning?", "Chinese")
    learner_level = st.select_slider("CEFR Level", ["A1", "A2", "B1", "B2", "C1", "C2"])
    conversation_context = st.text_area(
        "Do you have a specific context in mind?",
        placeholder="Ordering food at a restaurant",
    )
    translation_on = st.checkbox("Provide English translation?")


def generate_convo(
    vocab, practice_language, learner_level, conversation_context, translation_on
):
    # Instantiate LLM model
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

    # Refining the template to include language settings and conversation context
    translation_request = (
        "Also provide an English translation." if translation_on else ""
    )
    template = "In {practice_language}, create a small conversation at CEFR level {learner_level} using the word: '{vocab}'. Context: {conversation_context}. {translation_request} Make sure to use the word in context."

    prompt = PromptTemplate(
        input_variables=[
            "vocab",
            "practice_language",
            "learner_level",
            "conversation_context",
            "translation_request",
        ],
        template=template,
    )
    prompt_query = prompt.format(
        practice_language=practice_language,
        learner_level=learner_level,
        vocab=vocab,
        conversation_context=conversation_context,
        translation_request=translation_request,
    )

    # Run LLM model
    response = llm(prompt_query)

    # Append new response to the start of the list so it appears at the top
    st.session_state["responses"].insert(0, response)
    return response  # Now generate_convo returns the response but also stores it in session state

    # Print results
    # return st.info(response)


if "responses" not in st.session_state:
    st.session_state["responses"] = []

# UI for input outside of the settings, so users can submit words anytime.
with st.form("myform"):
    vocab_text = st.text_input(
        "Enter the word or words you want to see used in a conversation:",
        placeholder="Vocabulary",
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    # Call generate_convo with the input and settings anytime a word is submitted
    generate_convo(
        vocab_text,
        practice_language,
        learner_level,
        conversation_context,
        translation_on,
    )

# Display stored responses
for response in st.session_state["responses"]:
    st.info(response)

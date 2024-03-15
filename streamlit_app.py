import streamlit as st

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

google_api_key = st.secrets["GOOGLE_API_KEY"]

st.title("Conversation Dictionary")
st.caption(
    "Disclaimer: This dictionary may not always provide perfect translations or contextual examples; please cross-check and be prepared to explore different usage examples."
)


with st.sidebar:
    st.title("Language Settings")
    sidebar_tab1, sidebar_tab2 = st.tabs(["Details", "Feedback"])

    with sidebar_tab1:
        practice_language = st.text_input(
            "Target Language",
            placeholder="Chinese w/pinyin",
            help="Enter the language you're learning, e.g., Chinese, Spanish.",
        )
        learner_level = st.select_slider(
            "CEFR Level",
            ["A1", "A2", "B1", "B2", "C1", "C2"],
        )
        conversation_context = st.text_area(
            "Context",
            placeholder="Ordering food at a restaurant",
            help="Specify a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
        )
        formality = st.selectbox(
            "Formality",
            [
                "Balanced",
                "Informal",
                "Formal",
            ],
        )

    with sidebar_tab2:
        native_language = st.text_input(
            "Preferred Language",
            value="English",
            help="Set the language for the explanations.",
        )
        translation_on = st.toggle(
            f"{native_language} explanations",
            help=f"Check this to receive conversations with {native_language} translations and explinations.",
        )
        highlight_mistakes_on = st.toggle(
            "Show common mistakes",
            help="Check this to show common mistakes learners might make.",
        )


# Button to clear responses
if st.button("Clear All Responses"):
    st.session_state["responses"] = []  # Reset the list of responses


def refine_template(
    vocab,
    practice_language,
    learner_level,
    conversation_context,
    translation_on,
    formality,
    highlight_mistakes_on,
    preferred_language,
):
    translation_request = (
        "Provide a translation. Include explanations for cultural or contextual nuances where necessary"
        if translation_on
        else "Do not translate the dialogue."
    )
    mistakes_request = (
        f"Highlight common mistakes learners might make with '{vocab}', and rectify them by providing 2-3 exemplar sentences that correct these errors."
        if highlight_mistakes_on
        else ""
    )

    template = f"Construct a dialogue in {practice_language}, tailored to CEFR level {learner_level}, consisting of 3-5 exchanges. Your task is to weave the target word '{vocab}' into a scenario that fits the theme/context, {conversation_context}. Aim for a {formality} formality register. Begin with a brief description of the scenario in the students preferred_language, {preferred_language}. This setup should establish the theme/context and provide a backdrop for the dialogue. Make sure it's clear and engaging, setting the stage for the language interaction. {mistakes_request} {translation_request} "

    return template


def create_prompt(
    template,
    practice_language,
    learner_level,
    vocab,
    conversation_context,
    translation_request,
    formality,
    mistakes_request,
    preferred_language,
):
    prompt = PromptTemplate(
        input_variables=[
            "vocab",
            "practice_language",
            "learner_level",
            "conversation_context",
            "translation_request",
            "formality",
            "mistakes_request",
            "preferred_language",
        ],
        template=template,
    )
    prompt_query = prompt.format(
        practice_language=practice_language,
        learner_level=learner_level,
        vocab=vocab,
        conversation_context=conversation_context,
        translation_request=translation_request,
        formality=formality,
        mistakes_request=mistakes_request,
        preferred_language=preferred_language,
    )
    return prompt_query


def generate_convo(
    vocab,
    practice_language,
    learner_level,
    conversation_context,
    translation_on,
    formality,
    highlight_mistakes_on,
    preferred_language,
):

    if not vocab.strip():
        st.warning("Enter a vocabulary word.")
        return None
    if not practice_language.strip():
        st.warning("Set your langauge in the sidebar located at the top left.")
        return None

    try:
        # Instantiate LLM model
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

        template = refine_template(
            vocab,
            practice_language,
            learner_level,
            conversation_context,
            translation_on,
            formality,
            highlight_mistakes_on,
            preferred_language,
        )

        prompt_query = create_prompt(
            template,
            practice_language,
            learner_level,
            vocab,
            conversation_context,
            translation_on,
            formality,
            highlight_mistakes_on,
            preferred_language,
        )

        # Run LLM model
        response = llm(prompt_query)

        # Append new response to the start of the list so it appears at the top
        st.session_state["responses"].insert(0, response)

        # Limit the number of responses to a specific max value, e.g., 10
        max_responses = 5
        if len(st.session_state["responses"]) > max_responses:
            # Remove the oldest response(s) to maintain only a max number of responses
            st.session_state["responses"] = st.session_state["responses"][
                :max_responses
            ]

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None  # Return None if an exception occurred

    return response


if "responses" not in st.session_state:
    st.session_state["responses"] = []

# UI for input outside of the settings, so users can submit words anytime.
with st.form("myform"):
    vocab_text = st.text_input(
        "Enter the word or words you want to see used in a conversation:",
        placeholder="Vocabulary",
        help="Additional option in the sidebar located at the top left",
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner("Creating your dialogue..."):
        # Call generate_convo with the input and settings anytime a word is submitted
        generate_convo(
            vocab_text,
            practice_language,
            learner_level,
            conversation_context,
            translation_on,
            formality,
            highlight_mistakes_on,
            native_language,
        )

for response in st.session_state["responses"]:
    st.info(response)

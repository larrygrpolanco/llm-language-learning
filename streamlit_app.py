import streamlit as st

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

google_api_key = st.secrets["GOOGLE_API_KEY"]

st.title("Conversation Dictionary")
st.caption(
    "Disclaimer: this dictionary may not always provide perfect translations or contextual examples; please cross-check and be prepared to explore different usage examples."
)


with st.sidebar:
    st.title("Language Settings")
    practice_language = st.text_input(
        "Language",
        "Chinese",
        help="Enter the language you're learning, e.g., Chinese, Spanish.",
    )
    learner_level = st.select_slider(
        "CEFR Level",
        ["A1", "A2", "B1", "B2", "C1", "C2"],
        help="Select your current proficiency level according to the CEFR framework.",
    )
    conversation_context = st.text_area(
        "Context",
        placeholder="Ordering food at a restaurant",
        help="Specify a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
    )
    translation_on = st.toggle(
        "English translation",
        help="Check this to receive conversations with English translations.",
    )

# Button to clear responses
if st.button("Clear All Responses"):
    st.session_state["responses"] = []  # Reset the list of responses


def display_response(response):
    # Custom styling for the response display
    response_html = f"""
    <div style="border-left: 5px solid #4CAF50; background-color: #f2f2f2; padding: 10px; margin: 10px 0;">
        <p>{response}</p>
    </div>
    """
    st.markdown(response_html, unsafe_allow_html=True)


def refine_template(
    vocab, practice_language, learner_level, conversation_context, translation_on
):
    translation_request = (
        "Also provide an English translation. When providing the English translation, include explanations for cultural or contextual nuances where necessary"
        if translation_on
        else ""
    )
    template = f"In {practice_language}, create a concise, engaging conversation of about 3-5 exchanges at the CEFR level {learner_level}, using the word '{vocab}' in a context that is {conversation_context}. Please include a mixture of formal and informal uses if applicable. Highlight any common errors in the use of '{vocab}' and provide 2-3 sentences showcasing correct usage outside of the conversation.{translation_request}"
    return template


def create_prompt(
    template,
    practice_language,
    learner_level,
    vocab,
    conversation_context,
    translation_request,
):
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
    return prompt_query


def generate_convo(
    vocab, practice_language, learner_level, conversation_context, translation_on
):

    if not vocab.strip():
        st.error("Vocabulary cannot be empty.")
    if not practice_language.strip():
        st.error("Practice language cannot be empty.")

    # Instantiate LLM model
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

    template = refine_template(
        vocab, practice_language, learner_level, conversation_context, translation_on
    )

    prompt_query = create_prompt(
        template,
        practice_language,
        learner_level,
        vocab,
        conversation_context,
        translation_on,
    )

    # Run LLM model
    response = llm(prompt_query)

    # Append new response to the start of the list so it appears at the top
    st.session_state["responses"].insert(0, response)

    # Limit the number of responses to a specific max value, e.g., 10
    max_responses = 10
    if len(st.session_state["responses"]) > max_responses:
        # Remove the oldest response(s) to maintain only a max number of responses
        st.session_state["responses"] = st.session_state["responses"][:max_responses]

    return response  # Now generate_convo returns the response but also stores it in session state


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


# Edit with HTML
# for response in st.session_state["responses"]:
#     display_response(response)

import streamlit as st
from genai_processor import LanguageModelProcessor, ChatGPTProcessor, GeminiProcessor

st.page_link("Welcome.py", label="Home", icon="🏠")


st.title("💬 Conversation Dictionary", anchor="language-learning.streamlit.app")

st.markdown(
    "Have a word you want to see used in a conversation? Learning new words and phrases in context can help you understand and remember them better."
)
# st.caption(
#     "Disclaimer: This dictionary may not always provide perfect translations, contextual examples, or even the correct language; try resubmitting and be prepared to cross-check examples."
# )


with st.sidebar:
    # st.title("Language Settings")
    sidebar_tab1, sidebar_tab2 = st.tabs(["Settings", "Tools"])

    with sidebar_tab1:
        conversation_context = st.text_area(
            "Context",
            placeholder="Ordering food at a restaurant",
            help="Specify a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
        )
        formality = st.select_slider(
            "Formality",
            [
                "Informal",
                "Balanced",
                "Formal",
            ],
            value="Balanced",
        )
        st.divider()
        preferred_language = st.text_input(
            "Preferred Language",
            value="English",
            help="Set language for the explanations and translations (works best with English).",
        )
        translation_on = st.toggle(
            f"{preferred_language} explanations",
            help=f"Check this to request {preferred_language} translations and cultural explinations.",
        )
        highlight_mistakes_on = st.toggle(
            "Show common mistakes",
            help="Check this to show common mistakes learners might make.",
        )

    with sidebar_tab2:
        st.caption("Advanced Settings")
        st.caption("Changing these might break the app. Refresh the page to reset.")
        # LLM Selection
        llm_choice = st.selectbox(
            "Choose your Language Model",
            [
                "Google Gemini-Pro",
                "OpenAI ChatGPT 4",
                # "Meta LLama 2",
            ],  # Add other LLMs as needed
            index=0,  # Default to the first option
            help="Select the Language Model to generate conversations.",
        )

        template_editing = st.expander("Edit Prompt Template", expanded=False)
        with template_editing:
            user_template = st.text_area(
                "Edit the template used for generating conversations:",
                value="""# Example template:
"Construct a dialogue in {practice_language}, tailored to CEFR level {learner_level}, consisting of 3-5 exchanges. Your task is to weave the target word '{vocab}' into a scenario that fits the theme/context {conversation_context}. Aim for a {formality} formality register. Begin with a brief description of the scenario in the students preferred_language ({preferred_language}). This setup should establish the theme/context and provide a backdrop for the dialogue. Make sure it's clear and engaging, setting the stage for the language interaction. {mistakes_request} {translation_request} "
""",
                height=300,
                help="Modify the template as needed. This template will be used for generating conversations based on your settings. Do not change the {settings} in curly braces.",
            )
            if st.button("Save Template"):
                # Save the user modified template to session state or use it directly for generation
                st.session_state["user_template"] = user_template
                st.success("Template saved successfully!")


col1, col2, col3 = st.columns(3)
with col3:
    st.markdown("#")
    # Button to clear responses
    if st.button("Clear All Responses"):
        st.session_state["responses"] = []  # Reset the list of responses

with col1:
    practice_language = st.text_input(
        "Target Language",
        placeholder="e.g., Chinese, Spanish.",
        help="Enter the language you're learning.",
    )

with col2:
    learner_level = st.selectbox(
        "CEFR Level (Proficiency)",
        [
            "A1 Beginner",
            "A2 Pre-intermediate",
            "B1 Intermediate",
            "B2 Upper-Intermediate",
            "C1 Advanced",
            "C2 Mastery",
        ],
    )


# UI for input outside of the settings, so users can submit words anytime.
with st.form("myform"):
    vocab_text = st.text_input(
        "Enter the word or words you want to see used in a conversation:",
        placeholder="Vocabulary",
        help="Additional options in the sidebar located at the top left",
    )
    submitted = st.form_submit_button("Submit")


def process_user_template(template, settings):
    """
    Replace placeholders in the user template with actual settings values.

    :param template: The user-defined template string with placeholders.
    :param settings: A dictionary of settings values.
    :return: The processed template with placeholders filled in.
    """
    for key, value in settings.items():
        placeholder = f"{{{key}}}"  # Placeholders are expected in {key} format.
        if placeholder in template:
            template = template.replace(placeholder, str(value))
    return template


if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Ensure consistent use of keys and proper initialization
if "llm_processor" not in st.session_state:
    st.session_state["llm_processor"] = LanguageModelProcessor(
        st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
    )

# Updated to reflect the current settings
current_settings = {
    "conversation_context": conversation_context,
    "formality": formality,
    "preferred_language": preferred_language,
    "translation_on": translation_on,
    "highlight_mistakes_on": highlight_mistakes_on,
    "practice_language": practice_language,
    "learner_level": learner_level,
    "llm_choice": llm_choice,
    "custom_api_key": None,  # or the appropriate value
}

# Apply the settings to your processor
st.session_state["llm_processor"].set_settings(current_settings)

# Generating conversation using the corrected instance
if submitted:
    if not vocab_text.strip():
        st.warning("Enter a vocabulary word.")

    if not practice_language.strip():
        st.warning("Set your target langauge in the sidebar located at the top left.")

    with st.spinner("Creating your dialogue..."):
        if "user_template" in st.session_state:  # Check for user prompt
            user_template = st.session_state["user_template"]
            prompt = process_user_template(user_template, current_settings)
        else:
            prompt = st.session_state["llm_processor"].create_convo_prompt(vocab_text)

        # Run LLM model
        if llm_choice == "Google Gemini-Pro":
            gemini_processor = GeminiProcessor(
                st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
            )
            response = gemini_processor.generate_convo(prompt)
        elif llm_choice == "OpenAI ChatGPT 4":
            chatgpt_processor = ChatGPTProcessor(
                st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
            )
            response = chatgpt_processor.generate_convo(prompt)

        # Append new response to the start of the list so it appears at the top
        st.session_state["responses"].insert(0, response)

        # Limit the number of responses to a specific max value
        max_responses = 5
        if len(st.session_state["responses"]) > max_responses:
            # Remove the oldest response(s) to maintain only a max number of responses
            st.session_state["responses"] = st.session_state["responses"][
                :max_responses
            ]


for response in st.session_state["responses"]:
    st.info(response)

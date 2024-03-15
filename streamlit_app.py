import streamlit as st
from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

google_api_key = st.secrets["GOOGLE_API_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("Conversation Dictionary")

st.markdown(
    "Learning new words and phrases in context helps you understand and remember them better."
)
st.caption(
    "Disclaimer: This dictionary may not always provide perfect translations, contextual examples, or even the correct language; try resubmitting and be prepared to cross-check examples."
)


with st.sidebar:
    # st.title("Language Settings")
    sidebar_tab1, sidebar_tab2, sidebar_tab3 = st.tabs(["Settings", "Details", "Tools"])

    with sidebar_tab1:
        practice_language = st.text_input(
            "Target Language",
            placeholder="e.g., Chinese, Spanish.",
            help="Enter the language you're learning.",
        )
        learner_level = st.select_slider(
            "CEFR Level (Proficiency)",
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
            help="Set language for the explanations and translations (works best with English).",
        )
        translation_on = st.toggle(
            f"{native_language} explanations",
            help=f"Check this to request {native_language} translations and explinations.",
        )
        highlight_mistakes_on = st.toggle(
            "Show common mistakes",
            help="Check this to show common mistakes learners might make.",
        )

    with sidebar_tab3:
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
        st.divider()
        custom_api_key = st.text_input(
            "API Key", type="password", help="Use your personal API key."
        )
        st.divider()

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
        f"Alongside the dialogue, please provide a translation into the learner's preferred language ({preferred_language}). Emphasize clarity and accuracy in your translation. Where relevant, include brief annotations or explanations to highlight cultural or contextual nuances. These insights should elucidate expressions, idioms, or cultural references that may not directly translate but are crucial for understanding the dialogue's deeper meanings and implications."
        if translation_on
        else "Provide the dialogue with no translations. Focus on ensuring the dialogue is engaging and educational within the parameters set, allowing the learner to immerse fully in the practice language without direct translation. This approach encourages deeper language intuition and context-based understanding."
    )
    mistakes_request = (
        f"Identify common errors learners might commit when using the vocabulary word '{vocab}'. Illuminate these mistakes by providing a brief explanation of why they are incorrect. Enhance this learning moment by crafting 2-3 model sentences that demonstrate the correct usage of '{vocab}'. These sentences should not only rectify the identified mistakes but also serve as clear examples for learners to emulate, helping them to internalize the correct application of the word in various contexts."
        if highlight_mistakes_on
        else ""
    )

    template = f"""
"Create a dialogue in {practice_language}, tailored specifically to the CEFR level {learner_level}. Your objective is to seamlessly incorporate the target vocabulary word '{vocab}' into a conversation that is relevant to the given theme or context, '{conversation_context}'. Please adhere to the following guidelines to ensure a high-quality learning experience:

Scenario Introduction: Begin with a concise description of the scenario in the learner's preferred language, '{preferred_language}'. This description should be engaging and clear, setting the stage for the dialogue. Briefly outline the setting, characters involved, and the situation they are in, making sure it aligns with the theme/context '{conversation_context}'.

Dialogue Construction:

Compose 3-5 exchanges between characters in {practice_language}, ensuring the dialogue is realistic and relevant to the learners' experiences.
Integrate the target vocabulary word '{vocab}' naturally into the conversation. Use the word in different forms or contexts if possible to show its versatility.
Adjust the dialogue to match the specified {practice_language} CEFR level '{learner_level}', considering sentence complexity, vocabulary, and grammatical structures appropriate for that level.
Formality Register: Ensure the dialogue reflects the requested level of formality ('{formality}'). This could range from informal, using colloquial language and contractions, to formal, employing polite forms, professional terminology, and complete sentences.

Dialogue Length and Complexity: Aim for a total word count of approximately 100-150 words for the entire dialogue. This ensures enough {practice_language} content for educational value without overwhelming the learner. Sentences should vary in length and complexity according to the CEFR level specified.

Ensure that your {practice_language} dialogue is not only a learning tool but also a means for reflection and deeper engagement with the language. The goal is to make each dialogue a stepping stone towards fluency, providing learners with practical language skills they can apply in real-world situations.

{mistakes_request}

{translation_request}
"""

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
    llm_choice,
    custom_api_key,
):

    if not vocab.strip():
        st.warning("Enter a vocabulary word.")
        return None
    if not practice_language.strip():
        st.warning("Set your target langauge in the sidebar located at the top left.")
        return None

    try:
        # Choose the LLM based on user selection
        if llm_choice == "Google Gemini-Pro":
            # Use custom API key if provided, otherwise default to the stored API key
            effective_api_key = (
                custom_api_key if custom_api_key.strip() else google_api_key
            )
            llm = GoogleGenerativeAI(
                model="gemini-pro", google_api_key=effective_api_key
            )
        elif llm_choice == "OpenAI ChatGPT 4":
            # Use custom API key if provided, otherwise default to the stored API key
            effective_api_key = (
                custom_api_key if custom_api_key.strip() else openai_api_key
            )
            client = OpenAI(api_key=effective_api_key)
        elif llm_choice == "Meta LLama 2":
            # Instantiate LLama 2
            llm = None  # Placeholder for other LLM instantiation
        else:
            raise ValueError("Unsupported LLM selected")

        # Use the user-modified template if available
        if "user_template" in st.session_state:
            template = st.session_state["user_template"]
        else:
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
        if llm_choice == "Google Gemini-Pro":
            response = llm(prompt_query)
        elif llm_choice == "OpenAI ChatGPT 4":
            gpt_response_json = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_query}],
                model="gpt-4-turbo-preview",
            )
            response = gpt_response_json.choices[0].message.content

        # Append new response to the start of the list so it appears at the top
        st.session_state["responses"].insert(0, response)

        # Limit the number of responses to a specific max value
        max_responses = 3
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
        help="Additional options in the sidebar located at the top left",
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
            llm_choice,
            custom_api_key,
        )

for response in st.session_state["responses"]:
    st.info(response)

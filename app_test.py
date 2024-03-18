import streamlit as st

from word_lists import freq_colored_dict
from genai_processor import ChatGPTProcessor, GeminiProcessor



# ColorCoder class definition
class ColorCoder:
    def __init__(self, color_dict):
        self.color_dict = color_dict
        self.default_color = "#34495E"

    def colorize_text(self, text):
        words = text.split()  # Split the text into words
        colored_text = ""

        for word in words:
            uppercase_word = word.upper().strip(
                ".,!?"
            )  # Consider stripping punctuation for matching
            # Check if the word (or its uppercase variant) is in the dictionary
            if uppercase_word in self.color_dict:
                # Wrap the word in a span with the color style
                colored_word = f'<span style="color: {self.color_dict[uppercase_word]};">{word}</span>'
            else:
                colored_word = (
                    f'<span style="color: {self.default_color};">{word}</span>'
                )
            colored_text += (
                colored_word + " "
            )  # Reconstruct the sentence with colored words

        return colored_text


st.title("Comprehensible-izer", anchor="language-learning.streamlit.app")

st.markdown(
    "Reword sentences or passages to make them more comprehensible and appropriate for your level."
)
st.caption(
    "Disclaimer: This tool may not always provide perfect rewordings for your level; try resubmitting and try differnt things???"
)

with st.sidebar:
    (
        sidebar_tab1,
        sidebar_tab2,
    ) = st.tabs(["Key", "Tools"])
    with sidebar_tab1:
        st.title("Word Frequency Key")

        with st.expander("BNC/COCA Word Lists"):
            st.caption(
                "This color-coded key represents word difficulty based on their frequency in Paul Nation's BNC/COCA word family lists, which categorize word families based on frequency from the 1st to the 25th most frequent 1,000-word families, with colors ranging from green, the most common 1,000 word families in English, to black, words beyond the 6,000 most common word families."
            )

        # HTML template for displaying each color with text
        color_template = """
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <div style='width: 20px; height: 20px; background-color: {}; margin-right: 10px;'></div>
            <span>{}</span>
        </div>
        """

        # Dictionary of difficulty levels with their corresponding colors and adjusted descriptions
        difficulty_levels = {
            "1K": {
                "color": "#78AB46",
                "description": "Very common words you likely know.",
            },
            "2K": {
                "color": "#3498DB",
                "description": "Common words you probably know.",
            },
            "3K-4K": {
                "color": "#F1C40F",
                "description": "Fairly common words you might know.",
            },
            "5K-6K": {
                "color": "#E67E22",
                "description": "Less common, might be challenging.",
            },
            "7K-8K": {
                "color": "#E74C3C",
                "description": "Uncommon words that are more challenging.",
            },
            "9K-10K": {
                "color": "#9B59B6",
                "description": "Rare words that will be challenging.",
            },
            "11K+": {
                "color": "#34495E",
                "description": "Rare words, possibly very difficult.",
            },
        }

        # Loop through the dictionary and display each color with its description in the sidebar
        for level, info in difficulty_levels.items():
            color_block = color_template.format(
                info["color"], f"{level}: {info['description']}"
            )
            st.markdown(color_block, unsafe_allow_html=True)

    with sidebar_tab2:
        st.caption("Advanced Settings")
        st.caption("Changing these might break the app. Refresh the page to reset.")
        # LLM Selection
        llm_choice = st.selectbox(
            "Choose your Language Model",
            [
                "Google Gemini-Pro",
                "OpenAI ChatGPT 3.5",
                # "Meta LLama 2",
            ],  # Add other LLMs as needed
            index=0,  # Default to the first option
            help="Select the Language Model to generate conversations.",
        )
        st.divider()
        custom_api_key = st.text_input(
            "API Key", type="password", help="Use your personal API key."
        )


# App Main Body

tab1, tab2 = st.tabs(["Converter", "Info"])

with tab2:
    st.subheader("How does this work?")
    st.markdown(
        "A word family is a common unit of measurement in lexical demand studies. It consists of a base form (e.g., fault), its inflected forms (e.g., faults, faulted, faulting), and closely related derived forms (e.g., faultless, faultlessly, faulty, unfaulty)."
    )


with tab1:

    (
        col1,
        col2,
    ) = st.columns(2)

    with col1:
        learner_level = st.selectbox(
            "Select the appropriate proficiency level",
            options=[
                "A1 Beginner",
                "A2 Pre-intermediate",
                "B1 Intermediate",
                "B2 Upper-Intermediate",
                "C1 Advanced",
                "C2 Mastery",
                "Keep Orginal Text",
            ],
            label_visibility="visible",
            help="Select the level you want this to be simplified for.",
            index=6,
        )
        enable_color_coding = st.toggle(
            "Color coding",
            value=True,
            help="Color words by difficuty (key in top left sidebar).",
        )
        st.markdown("#")
        st.markdown("#")
        # Button to clear responses
        if st.button("Clear All Responses"):
            st.session_state["response_history"] = []  # Reset the list of responses

    with col2:
        with st.form("myform"):
            orginal_text = st.text_area(
                label="Paste here:",
                value="Most people who bother with the matter at all would admit that the English language is in a bad way, but it is generally assumed that we cannot by conscious action do anything about it. Our civilization is decadent and our language – so the argument runs – must inevitably share in the general collapse. It follows that any struggle against the abuse of language is a sentimental archaism, like preferring candles to electric light or hansom cabs to aeroplanes. Underneath this lies the half-conscious belief that language is a natural growth and not an instrument which we shape for our own purposes.",
                help="Paste any text e.g., Orwell's Politics and the English Language.",
            )
            submitted = st.form_submit_button("Submit")

# st.divider()

if "response_history" not in st.session_state:
    st.session_state.response_history = []

color_coder = ColorCoder(freq_colored_dict)

# Initialize the correct processor based on user choice
if llm_choice == "OpenAI ChatGPT 3.5":
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    # Use custom API key if provided, otherwise default to the stored API key
    effective_api_key = custom_api_key if custom_api_key.strip() else openai_api_key
    chatgpt_processor = ChatGPTProcessor(openai_api_key)
elif llm_choice == "Google Gemini-Pro":
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    effective_api_key = custom_api_key if custom_api_key.strip() else google_api_key
    gemini_processor = GeminiProcessor(google_api_key)

if submitted:
    with st.spinner("Comprehensible-izing"):
        if learner_level != "Keep Orginal Text":
            if llm_choice == "OpenAI ChatGPT 3.5":
                simplified_text = chatgpt_processor.simplify_text(
                    orginal_text, learner_level
                )
            elif llm_choice == "Google Gemini-Pro":
                simplified_text = gemini_processor.simplify_text(
                    orginal_text, learner_level
                )
        else:
            simplified_text = orginal_text

        if enable_color_coding:
            # Color code the simplified text
            colored_text = color_coder.colorize_text(simplified_text)
        else:
            # Display the simplified text without color coding
            colored_text = simplified_text

        st.session_state.response_history.insert(0, colored_text)

        # Limit the history to the most recent 5 responses
        st.session_state.response_history = st.session_state.response_history[:5]

# Display each response from the session state
for response in st.session_state.response_history:
    # Wrap each response with your styled div
    text_with_background = f'<div style="background-color: #F5F5F5; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-family: Arial, sans-serif; color: #333; line-height: 1.5;">{response}</div>'
    st.markdown(text_with_background, unsafe_allow_html=True)

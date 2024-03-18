import streamlit as st

from word_lists import freq_colored_dict
from openai import OpenAI


# ColorCoder class definition
class ColorCoder:
    def __init__(self, color_dict):
        self.color_dict = color_dict

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
                colored_word = word
            colored_text += (
                colored_word + " "
            )  # Reconstruct the sentence with colored words

        return colored_text


st.title("Comprehensible-izer", anchor="language-learning.streamlit.app")

st.markdown(
    "Make sentences or passages harder or easier to be more comprehensible and appropriate for your level."
)
st.caption(
    "Disclaimer: This tool may not always provide perfect rewordings for your level; try resubmitting and try differnt things???"
)


tab1, tab2 = st.tabs(["Converter", "Info"])

with tab2:
    st.subheader("How does this work?")


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
            ],
            label_visibility="visible",
        )
        st.markdown("More information about word families?")

    with col2:
        with st.form("myform"):
            orginal_text = st.text_area(
                label="Paste here:",
                value="Most people who bother with the matter at all would admit that the English language is in a bad way, but it is generally assumed that we cannot by conscious action do anything about it. Our civilization is decadent and our language – so the argument runs – must inevitably share in the general collapse. It follows that any struggle against the abuse of language is a sentimental archaism, like preferring candles to electric light or hansom cabs to aeroplanes. Underneath this lies the half-conscious belief that language is a natural growth and not an instrument which we shape for our own purposes.",
                help="Paste any text e.g., Orwell's Politics and the English Language.",
            )
            submitted = st.form_submit_button("Submit")

    st.divider()

    color_coder = ColorCoder(freq_colored_dict)

    if submitted:
        colored_text = color_coder.colorize_text(orginal_text)
        text_with_background = f'<div style="background-color: #f0f2f6; padding: 10px;">{colored_text}</div>'  # apply background This is so much fucking work...
        st.markdown(text_with_background, unsafe_allow_html=True)

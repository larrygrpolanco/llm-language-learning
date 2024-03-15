Simple web app for practicing vocabulary. This app utilizes langchain and Google's gemini API.

Possible future implimitations:

# This highlights the word but does not save chat and does not look great

# def highlight_vocabulary(response, vocab):

# highlighted_response = response.replace(vocab, f"<mark>{vocab}</mark>")

# return highlighted_response

# for response in st.session_state["responses"]:

# highlighted_response = highlight_vocabulary(response, vocab_text)

# st.markdown(highlighted_response, unsafe_allow_html=True)

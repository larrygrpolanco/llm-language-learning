Simple web app for practicing vocabulary. This app utilizes langchain and Google's gemini API.

Possible future implimitations:

# This highlights the word but does not save chat and does not look great

# def highlight_vocabulary(response, vocab):

# highlighted_response = response.replace(vocab, f"<mark>{vocab}</mark>")

# return highlighted_response

# for response in st.session_state["responses"]:

# highlighted_response = highlight_vocabulary(response, vocab_text)

# st.markdown(highlighted_response, unsafe_allow_html=True)

# Simple template

# template = f"Construct a dialogue in {practice_language}, tailored to CEFR level {learner_level}, consisting of 3-5 exchanges. Your task is to weave the target word '{vocab}' into a scenario that fits the theme/context, {conversation_context}. Aim for a {formality} formality register. Begin with a brief description of the scenario in the students preferred_language, {preferred_language}. This setup should establish the theme/context and provide a backdrop for the dialogue. Make sure it's clear and engaging, setting the stage for the language interaction. {mistakes_request} {translation_request} "


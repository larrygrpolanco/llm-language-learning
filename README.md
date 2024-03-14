Simple web app for practicing vocabulary. This app utilizes langchain and Google's gemini API.


Possible future implimitations:
# This highlights the word but does not save chat and does not look great
# def highlight_vocabulary(response, vocab):
#     highlighted_response = response.replace(vocab, f"<mark>{vocab}</mark>")
#     return highlighted_response
# for response in st.session_state["responses"]:
#     highlighted_response = highlight_vocabulary(response, vocab_text)
#     st.markdown(highlighted_response, unsafe_allow_html=True)

# Complicated template
#     template = """
# Create a dialogue that will serve as a valuable language learning exercise. Each dialogue should be tailored specifically to the needs and context provided below, ensuring a meaningful and engaging practice scenario for the learner. Follow the structured format meticulously to achieve the best educational outcome.

# Parameters:

# Practice Language: {practice_language} (The language in which the dialogue should be written.)
# CEFR Level: {learner_level} (The proficiency level of the learner, as defined by the Common European Framework of Reference for Languages)
# Target Word: {vocab} (A specific vocabulary word that must be incorporated into the dialogue to help the learner understand its use in context.)
# Theme/Context: {conversation_context} (The situational context or theme within which the dialogue should take place, offering a realistic and relatable scenario for using the target language.)
# Formality Register: {formality} (The degree of formality appropriate for the dialogue, guiding the tone and linguistic choices.)
# Instructions for Generation:

# {mistakes_request}
# {translation_request}

# Scenario Setup: Begin with a brief description of the scenario. This setup should establish the theme/context and provide a backdrop for the dialogue. Make sure it's clear and engaging, setting the stage for the language interaction.

# Dialogue Construction: Following the scenario setup, craft a dialogue consisting of 3-5 exchanges between characters. Ensure the dialogue:

# Flows naturally and realistically within the established scenario.
# Appropriately incorporates the target word, showcasing its use in context.
# Adheres to the specified CEFR level, making it accessible and beneficial for the learner's proficiency stage.
# Observes the defined formality register, whether informal, formal, or somewhere in between, to suit the scenario and learning objectives.

# Objective: The primary goal of this exercise is to provide language learners with a practical, context-rich scenario in which they can see language in action. Through engaging with these dialogues, learners should be able to better grasp the nuances of the practice language, the application of the target word, and the dynamics of conversational exchanges at their CEFR level.
# """
import openai
import google.generativeai as gemini
import streamlit as st


class ChatGPTProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def simplify_text(
        self,
        text,
        learner_level,
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=-1.0,
        presence_penalty=-1.0,
    ):
        """
        Uses ChatGPT to simplify the given text to make it more comprehensible for English language learners, taking into account the learner's proficiency level.

        Parameters:
        - text (str): The text to be simplified.
        - learner_level (str): The proficiency level of the learner (e.g., "A1 Beginner", "B2 Upper-Intermediate").
        - temperature (float): Controls randomness in the output.
        - max_tokens (int): The maximum number of tokens to generate.
        - top_p (float): Nucleus sampling parameter alternative to temprature.
        - frequency_penalty (float): Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        - presence_penalty (float): Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

        Returns:
        - str: The simplified text.
        """
        # Tailor the prompt based on the learner level
        level_prompt = {
            "A1 Beginner": "very simple English",
            "A2 Pre-intermediate": "simple English",
            "B1 Intermediate": "moderately simple English",
            "B2 Upper-Intermediate": "intermediate English",
            "C1 Advanced": "advanced English",
            "C2 Mastery": "highly advanced English",
        }.get(
            learner_level, "simple English"
        )  # Default to simple English if level not matched

        prompt_text = f"Simplify this text into {level_prompt} for English language learners: {text}"

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt_text},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in simplifying text: {e}")
            return text


class GeminiProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        gemini.configure(api_key=self.api_key)

    def simplify_text(
        self,
        text,
        learner_level,
    ):

        # Tailor the prompt based on the learner level
        level_prompt = {
            "A1 Beginner": "very simple English",
            "A2 Pre-intermediate": "simple English",
            "B1 Intermediate": "moderately simple English",
            "B2 Upper-Intermediate": "intermediate English",
            "C1 Advanced": "advanced English",
            "C2 Mastery": "highly advanced English",
        }.get(
            learner_level, "simple English"
        )  # Default to simple English if level not matched

        prompt_text = f"Simplify this text into {level_prompt} for English language learners: {text}"

        model = gemini.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt_text)

        return response.text

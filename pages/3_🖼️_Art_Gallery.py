import streamlit as st
from openai import OpenAI
import openai


class ArtGallery:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_image_prompt(self, style):
        system_instructions = f"Craft Dall-E prompt for easily recognizable paintings in {style} style, for an image description game for English learners. Focus on a clear, simple noun (thing, or animal), avoid people. Use straightforward English and easy vocabulary to aid guessing and understanding, as if explaining the art to someone who hasn't seen it. Follow these steps. Step 1: Provide a descriptive title. Step 2: Provide a simple but comprehensive description of what is happening in the painting in 15 words or less"

        user_prompt = "Create an art gallery piece scene description."

        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": system_instructions,
                    },
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=50,
                temperature=0.9,
            )

            painting_prompt = response.choices[0].message.content

            return painting_prompt

        except Exception as e:
            print(f"Error in generating conversation: {e}")
        return None

    def generate_artwork(self, prompt, style, style_characteristics):
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=f"Create an image that clearly and vividly represents the following scene in the style of {style}, "
                f"which is known for its {style_characteristics}. The scene description is: '{prompt}'. "
                "Ensure the image is simple enough to be guessed or described by someone learning English, "
                "focus on the elements in the description only. There should be no words in the image",
                size="256x256",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            # print("Generated Image URL:", image_url)
            return image_url

        except openai.OpenAIError as e:
            print(e.http_status)
            print(e.error)


st.page_link("Welcome.py", label="Home", icon="🏠")


st.title("🖼️ Reading Art (Gallery)")

st.subheader("Try to recreate pieces of 'art' by describing them.")
st.markdown(
    "Language is only one meaning making system among many including painting, music, and dance. There are so many forms of literacy and reading images is one of them."
)
# st.markdown(
#     "the changing constructions of literacy within new technologies will require all of us to keep up with these changes and to prepare students for a vastly different conception of what it means to become literate (Leu et al., 2004, p. 1591)."
# )

with st.expander("Instructions"):
    st.caption("1. Select a style and click 'Enter Gallery' to begin.")
    st.caption(
        "2. Click 'See paintings' to create a paintings based off the secret gallery description."
    )
    st.caption("3. Try to recreate the painting by 'describing what you see'.")
    st.caption(
        "4. You can always click the 'show desciption button to see the orginal description."
    )
    st.caption(
        "The goal is not get the same painting, as you will get a different painting every time, the point is to play with and examine how language describes art."
    )

art_gallery = ArtGallery(st.secrets["OPENAI_API_KEY"])


# Check for existing session state or initialize it
if "gallery_entered" not in st.session_state:
    st.session_state["gallery_entered"] = False

if "ai_art_works" not in st.session_state:
    st.session_state["ai_art_works"] = []

if "player_arts" not in st.session_state:
    st.session_state["player_arts"] = []

if "ai_art_works_descriptions" not in st.session_state:
    st.session_state["ai_art_works_descriptions"] = []

if "player_arts_descriptions" not in st.session_state:
    st.session_state["player_arts_descriptions"] = []


choosen_style = st.selectbox(
    "Pick a style:",
    [
        "Renaissance",
        "Abstract Expressionism",
        "Art Deco",
        "Art Nouveau",
        "Avant-garde",
        "Baroque",
        "Classicism",
        "Digital Art",
        "Expressionism",
        "Futurism",
        "Harlem Renaissance",
    ],
    help="Paintings may not always follow this style.",
)

style_characteristics = {
    "Renaissance": "Realistic, detailed, perspective-focused",
    "Abstract Expressionism": "Spontaneous, emotional, non-representational",
    "Art Deco": "Geometric, streamlined, decorative",
    "Art Nouveau": "Flowing, organic, ornamental",
    "Avant-garde": "Innovative, non-traditional, experimental",
    "Baroque": "Dramatic, intense, detailed",
    "Classicism": "Harmonious, proportionate, idealized",
    "Digital Art": "Pixel-based, computer-generated, versatile",
    "Expressionism": "Distorted, subjective, emotive",
    "Futurism": "Dynamic, mechanical, motion-focused",
    "Harlem Renaissance": "Cultural, vibrant, expressive",
}

choosen_style_characteristics = style_characteristics[choosen_style]

if st.button("Enter New Gallery"):
    st.session_state["gallery_entered"] = True
    st.session_state["ai_art_works"] = []
    st.session_state["player_arts"] = []
    st.session_state["ai_art_works_descriptions"] = []
    st.session_state["player_arts_descriptions"] = []

    with st.spinner("Curating gallery..."):
        new_prompt = art_gallery.generate_image_prompt(style=choosen_style)
        if new_prompt:  # Ensure there's a new prompt
            st.session_state.ai_art_works_descriptions.append(new_prompt)

    with st.spinner("Hanging up paintings..."):
        if st.session_state.ai_art_works_descriptions:
            prompt = st.session_state.ai_art_works_descriptions[
                -1
            ]  # Use the latest prompt
            # Append the new artwork URL to the session state list
            st.session_state.ai_art_works.append(
                art_gallery.generate_artwork(
                    prompt,
                    style=choosen_style,
                    style_characteristics=choosen_style_characteristics,
                )
            )


if st.session_state["gallery_entered"]:
    st.divider()
    # New Prompt Generation
    col1, col2 = st.columns(2)

    with col1:

        if st.button("See More Paintings"):
            if st.session_state.ai_art_works_descriptions:
                prompt = st.session_state.ai_art_works_descriptions[
                    -1
                ]  # Use the latest prompt
                # Append the new artwork URL to the session state list
                st.session_state.ai_art_works.append(
                    art_gallery.generate_artwork(
                        prompt,
                        style=choosen_style,
                        style_characteristics=choosen_style_characteristics,
                    )
                )

        if st.toggle(
            "Show Gallery Description",
            help="Show the prompt to check to see if your description was close.",
        ):
            if st.session_state.ai_art_works_descriptions:
                st.markdown(f"{st.session_state.ai_art_works_descriptions[-1]}")
            else:
                st.write("No description available. Generate a new prompt.")

    with col2:
        player_description = st.text_input(
            "Describe what you see",
            placeholder="Lady with her hands crossed kind of smiling",
        )
        if st.button("Create Painting"):
            # Append the new artwork to the session state list
            st.session_state.player_arts.append(
                art_gallery.generate_artwork(
                    player_description,
                    style=choosen_style,
                    style_characteristics=choosen_style_characteristics,
                )
            )

    st.divider()

    paint_ai, paint_player = st.columns(2)

    # Displaying the gallery using session state lists
    with paint_ai:
        st.subheader("Gallery")
        # Reverse the list for display
        for ai_art_work in reversed(st.session_state.ai_art_works):
            st.image(ai_art_work)
        if not st.session_state.ai_art_works:
            st.write("Waiting for player to generate AI artwork...")

        if st.button("Leave this gallery"):
            st.session_state["gallery_entered"] = False
            st.caption("Are you sure?")
            st.caption("Click again to confirm.")

    with paint_player:
        st.subheader("Your Paintings")
        # Reverse the list for display
        for player_art in reversed(st.session_state.player_arts):
            st.image(player_art)
        if not st.session_state.player_arts:
            st.write("Waiting for player to submit description...")

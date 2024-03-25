import streamlit as st
from openai import OpenAI
import openai


class ArtGallery:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_image_prompt(self, style):
        system_instructions = (
            "Imagine you are creating prompts for Dall-E to generate paintings. The topic and theme of the art piece should be intersting and unique, but easy to guess. The topic should be common topics found in {style} style paintings."
            "These prompts will be used in an image reading/describing game for English language learners. "
            "Generate a prompt that describes an art piece. Include an noun (person, thing, or animal) as the main object."
            "Use basic English to make it easy for beginners to understand and guess. Avoid adjectives. "
            "Think of a very simple descriptions someone would use to describe a piece of art they saw in a gallery"
        )

        user_prompt = (
            "Create an art gallery piece scene description in 10 words or less."
        )

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
                max_tokens=30,
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


st.title("🖼️ Reading Art (Gallery)")

st.subheader("Try to recreate a piece of 'art' by describing it.")
st.markdown(
    "Language is only one meaning making system among many including painting, music, and dance. There are so many forms of literacy and reading images is one of them."
)
# st.markdown(
#     "the changing constructions of literacy within new technologies will require all of us to keep up with these changes and to prepare students for a vastly different conception of what it means to become literate (Leu et al., 2004, p. 1591)."
# )

with st.expander("Instructions"):
    st.caption(
        "1. Select a style and click 'Enter Gallery' to begin and set the theme."
    )
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
)

style_characteristics = {
    "Renaissance": "Focused on the revival of classical culture, emphasizing humanism, proportion, perspective, and the realistic depiction of the human body.",
    "Abstract Expressionism": "Emphasizes spontaneous, automatic, or subconscious creation with abstract forms and an emphasis on dynamic, gestural brushwork.",
    "Art Deco": "Known for its bold geometric shapes, rich colors, and lavish ornamentation, reflecting the modernity of the machine age.",
    "Art Nouveau": "Characterized by its use of long, sinuous, organic lines and was often inspired by natural forms.",
    "Avant-garde": "Refers to the innovative, experimental, and unconventional works or artists that push the boundaries of what is accepted as the norm or the status quo.",
    "Baroque": "Features dramatic use of light and shadow, rich colors, and grandeur, often with a sense of movement and emotional intensity.",
    "Classicism": "Emphasizes harmony, proportion, and disciplined expression, inspired by the art and culture of ancient Greece and Rome.",
    "Digital Art": "Artistic work or practice that uses digital technology as part of the creative or presentation process.",
    "Expressionism": "Seeks to express emotional experience rather than impressions of the external world, often through distorted, exaggerated, and vivid imagery.",
    "Futurism": "Focused on the dynamic quality of modern technological life, emphasizing speed, movement, and the machine as art.",
    "Harlem Renaissance": "A cultural movement that celebrated African American cultural, social, and artistic expressions, flourishing in the 1920s and 1930s in Harlem, New York.",
}

choosen_style_characteristics = style_characteristics[choosen_style]

if st.button("Enter New Gallery"):
    st.session_state["gallery_entered"] = True
    st.session_state["ai_art_works"] = []
    st.session_state["player_arts"] = []
    st.session_state["ai_art_works_descriptions"] = []
    st.session_state["player_arts_descriptions"] = []

    new_prompt = art_gallery.generate_image_prompt(style=choosen_style)
    if new_prompt:  # Ensure there's a new prompt
        st.session_state.ai_art_works_descriptions.append(new_prompt)


if st.session_state["gallery_entered"]:
    st.divider()
    # New Prompt Generation
    col1, col2 = st.columns(2)

    with col1:

        if st.button("See Paintings"):
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
                st.markdown(
                    f"**Description:** {st.session_state.ai_art_works_descriptions[-1]}"
                )
            else:
                st.write("No description available. Generate a new prompt.")

    with col2:
        player_description = st.text_input(
            "Describe what you see",
            placeholder="Lady with her hands crossed kind of smiling ",
        )
        if st.button("submit"):
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

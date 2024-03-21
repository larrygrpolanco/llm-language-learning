import streamlit as st
from openai import OpenAI
import openai


class ArtGallery:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_artwork(self, prompt):
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:{prompt}",
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

st.markdown(
    "Language is only one meaning making system among many inclduing painting, music, and dance. There are so many forms of literacy and reading images is one of them."
)
st.markdown(
    "the changing constructions of literacy within new technologies will require all of us to keep up with these changes and to prepare students for a vastly different conception of what it means to become literate (Leu et al., 2004, p. 1591)."
)
st.caption(
    "Disclaimer: The goal is not get the same image, as the same prompt will give you a different image everytime, the point is to play with and examine how language describes art."
)

st.divider()

art_gallery = ArtGallery(st.secrets["OPENAI_API_KEY"])


col1, col2 = st.columns(2)

# Form submit button?
with col1:
    make_new_painting = st.button("Generate Paiting")
    # art_gallery.generate_artwork("Rabbits in gladiator armor")

    #     st.image(art_work)


with col2:
    player_description = st.text_input(
        "Describe what you see", placeholder="So much pain..."
    )
    if st.button("submit"):
        player_art = art_gallery.generate_artwork(player_description)

        st.image(player_art)

    st.image(
        "https://oaidalleapiprodscus.blob.core.windows.net/private/org-UlEJpHGgSjvCkdBuTljkXbro/user-OmhqT7UpzJYh5xacslXM5fHi/img-P39bLjwVSphrG7sBBhnM9b6y.png?st=2024-03-21T00%3A42%3A42Z&se=2024-03-21T02%3A42%3A42Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-03-20T23%3A51%3A51Z&ske=2024-03-21T23%3A51%3A51Z&sks=b&skv=2021-08-06&sig=OcpBmsUe2T9KTPF4ouvMOKxCr1265Z/lWlaEM1dA6DQ%3D"
    )

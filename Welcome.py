import streamlit as st


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.title("Welcome! 👋", anchor="language-learning.streamlit.app")

st.markdown("Hello, my name is Larry Grullon-Polanco. I am a langauge teacher.")
st.markdown(
    "This are a just a collection of projects where I try to combine second language acquisition research and pedagogy with large language models such as OpenAI's ChatGPT and Google's Gemini."
)

st.divider()

st.subheader("Citations:")
with st.expander("Conversation Dictionary"):
    st.caption(
        "* Malone, J. (2018). Incidental vocabulary learning in SLA: Effects of frequency, aural enhancement, and working memory. Studies in Second Language Acquisition, 40(3), 651-675."
    )
    st.caption(
        "* Laufer, B. (2009). Second language vocabulary acquisition from language input and from form-focused activities. Language teaching, 42(3), 341-354."
    )

with st.expander("Comprehensible-izer"):
    st.caption(
        "* Rets, I., Astruc, L., Coughlan, T., & Stickler, U. (2022). Approaches to simplifying academic texts in English: English teachers’ views and practices. English for Specific Purposes, 68, 31-46."
    )
    st.caption(
        "* Vajjala, S., & Meurers, D. (2014). Readability assessment for text simplification: From analysing documents to identifying sentential simplifications. ITL-International Journal of Applied Linguistics, 165(2), 194-222."
    )

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

st.subheader("Refrences")
col1, col2 = st.columns(2)
with col1:
    st.title("Tools")
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

with col2:
    st.title("Games")
    with st.expander("Reading Art (Gallery)"):
        st.caption(
            "Unsworth, L. (2014). Multiliteracies and Metalanguage:: Describing Image/Text Relations as a Resource for Negotiating Multimodal Texts. In Handbook of research on new literacies (pp. 377-406). Routledge."
        )
        st.caption(
            "Leu, D. J., Kinzer, C. K., Coiro, J. L., & Cammack, D. W. (2004). Toward a theory of new literacies emerging from the Internet and other information and communication technologies. Theoretical models and processes of reading, 5(1), 1570-1613."
        )

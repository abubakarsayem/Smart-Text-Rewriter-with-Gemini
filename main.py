import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

template = """
Below is a draft text that may be poorly worded.
Your goal is to:
- Refine and improve the clarity, grammar, and style of the draft text
- Rewrite the text in the specified tone, making it suitable for the intended audience (e.g., formal, informal, or creative)
- Adapt the text to the specified dialect (e.g., American or British English) while maintaining the original meaning

Examples of Tones:
- Formal: Recent studies indicate that implementing regular physical activity significantly improves cognitive performance in adolescents. These findings suggest a strong correlation between exercise and academic achievement.
- Creative: Imagine unlocking your full potential just by moving your body! Research shows that every step, stretch, and jump fuels your brain, helping you ace those exams and feel amazing.
- Informal: Want to boost your brainpower? Studies show that staying active can help you think sharper and do better in school—let’s get moving!

Examples of Dialects:
- American: email, marketing campaign, website, feedback, smartphone, schedule, cookie, elevator, parking lot, fall
- British: e-mail, marketing campaign, website, feedback, mobile phone, timetable, biscuit, lift, car park, autumn

Instructions:
- Start with a warm introduction if needed.
- Maintain the meaning of the draft text.
- Rewrite the draft text in the specified TONE and DIALECT.

Only provide output. Do not output anything like "Here's a creative take on your draft, adapted for a British audience:" and so on.

Draft Text: {draft}
Tone: {tone}
Dialect: {dialect}

Your {dialect} response:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)

def load_LLM(api_key: str):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7
    )

st.set_page_config(page_title="Smart Text Rewriter with Gemini")
st.header("Smart Text Rewriter with Gemini")

col1, col2 = st.columns(2)
with col1:
    st.markdown("Re-write your text in different styles.")
with col2:
    st.write("Visit My Portfolio Site: [Abu Bakar Sayem](https://abmsayem.pages.dev)")

st.markdown("#### Enter Your Gemini API Key")
gemini_key = st.text_input("", placeholder="Ex: AIzaS......", type="password", label_visibility="collapsed")

st.markdown("#### Enter Your Text:")
draft_input = st.text_area("", placeholder="Your Text...", height=150, label_visibility="collapsed")

if len(draft_input.split()) > 1000:
    st.warning("Please enter a shorter text. Maximum 1000 words.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.markdown("<p style='font-size:18px; font-weight:700;'>Which tone would you like?</p>", unsafe_allow_html=True)
    option_tone = st.selectbox("", ('Formal', 'Creative', 'Informal'), label_visibility="collapsed")
with col2:
    st.markdown("<p style='font-size:18px; font-weight:700;'>Which Dialect would you like?</p>", unsafe_allow_html=True)
    option_dialect = st.selectbox("", ('American', 'British'), label_visibility="collapsed")

generate = st.button("Enter")

st.markdown("#### Your Re-written text:")
output_placeholder = st.empty()

if generate:
    if not gemini_key:
        st.warning("Please insert Gemini API Key.", icon="⚠️")
        st.stop()

    llm = load_LLM(gemini_key)

    prompt_with_draft = prompt.format(
        tone=option_tone,
        dialect=option_dialect,
        draft=draft_input
    )

    with st.spinner("Generating your re-written text..."):
        improved_redaction = llm.invoke(prompt_with_draft)

    output_placeholder.write(improved_redaction.content)

# 📚 Personalized Learning Platform (FINAL VERSION)

import streamlit as st
import wikipedia
from gtts import gTTS
import time

# -------------------------------
# 🎨 UI Styling
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #dbeafe, #fef9c3);
}
h1 {
    text-align: center;
    color: #1e3a8a;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.card {
    padding: 15px;
    background-color: #f1f5f9;
    border-radius: 12px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎓 Personalized Learning Platform</h1>", unsafe_allow_html=True)

# -------------------------------
# 🔍 GET SUGGESTIONS
# -------------------------------
@st.cache_data
def get_suggestions(query):
    try:
        return wikipedia.search(query)
    except:
        return []

# -------------------------------
# 🧠 GET NOTES (SMART)
# -------------------------------
@st.cache_data
def get_notes(topic):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        return wikipedia.summary(page.title, sentences=5)
    except:
        try:
            results = wikipedia.search(topic)
            if not results:
                return "No results found."
            return wikipedia.summary(results[0], sentences=5)
        except:
            return "Could not fetch information."

# -------------------------------
# 🖼️ GET IMAGES
# -------------------------------
@st.cache_data
def get_images(topic):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        images = page.images
        valid = [img for img in images if img.endswith((".jpg", ".png"))]
        return valid[:2]   # reduced for speed
    except:
        return []

# -------------------------------
# 🎤 VOICE
# -------------------------------
def speak(text):
    filename = f"voice_{int(time.time())}.mp3"
    tts = gTTS(text)
    tts.save(filename)
    with open(filename, "rb") as f:
        st.audio(f.read(), format="audio/mp3")

# -------------------------------
# 💾 SESSION STATE
# -------------------------------
if "notes" not in st.session_state:
    st.session_state.notes = ""

# -------------------------------
# 📥 INPUT + SUGGESTIONS
# -------------------------------
query = st.text_input("📘 Enter a Topic")

selected_topic = ""

if query:
    suggestions = get_suggestions(query)

    if suggestions:
        selected_topic = st.selectbox("🔎 Select Topic:", suggestions)
    else:
        st.warning("No suggestions found")

# -------------------------------
# 📚 TEACH BUTTON
# -------------------------------
if st.button("📚 Teach Me"):
    if selected_topic == "":
        st.warning("Please select a topic")
    else:
        st.session_state.notes = get_notes(selected_topic)

# -------------------------------
# 📘 DISPLAY
# -------------------------------
if st.session_state.notes:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📖 Explanation")
    st.write(st.session_state.notes)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔊 Listen Explanation"):
        speak(st.session_state.notes)

    # 🖼️ Images
    with st.spinner("Loading images..."):
        images = get_images(selected_topic)

    if images:
        st.subheader("🖼️ Related Images")
        cols = st.columns(len(images))
        for i, img in enumerate(images):
            cols[i].image(img, width=250)
    else:
        st.info("No images found.")

# -------------------------------
# ❓ DOUBT SECTION
# -------------------------------
st.subheader("❓ Ask Your Doubt")

question = st.text_input("Type your question")

@st.cache_data
def get_answer(question):
    try:
        results = wikipedia.search(question)
        if not results:
            return "No answer found."
        return wikipedia.summary(results[0], sentences=3)
    except:
        return "Try asking clearly."

if st.button("💡 Get Answer"):
    if question.strip() == "":
        st.warning("Enter a question")
    else:
        st.session_state.answer = get_answer(question)

if "answer" in st.session_state and st.session_state.answer:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📗 Answer")
    st.write(st.session_state.answer)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔊 Listen Answer"):
        speak(st.session_state.answer)

# -------------------------------
# 🎉 FOOTER
# -------------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Personalized Learning Platform | Final Version
</p>
""", unsafe_allow_html=True)

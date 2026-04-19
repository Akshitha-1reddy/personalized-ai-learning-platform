# 📚 Personalized Learning Platform (FINAL VERSION WITH ADVANCED QUIZ)

import streamlit as st
import wikipedia
from gtts import gTTS
import time
import random

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
# 🔍 Suggestions
# -------------------------------
@st.cache_data
def get_suggestions(query):
    try:
        return wikipedia.search(query)
    except:
        return []

# -------------------------------
# 🧠 Notes
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
# 🖼️ Images
# -------------------------------
@st.cache_data
def get_images(topic):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        images = page.images
        valid = [img for img in images if img.endswith((".jpg", ".png"))]
        return valid[:2]
    except:
        return []

# -------------------------------
# 🎤 Voice
# -------------------------------
def speak(text):
    filename = f"voice_{int(time.time())}.mp3"
    tts = gTTS(text)
    tts.save(filename)
    with open(filename, "rb") as f:
        st.audio(f.read(), format="audio/mp3")

# -------------------------------
# 🧠 Advanced Quiz Generator
# -------------------------------
def generate_advanced_quiz(text):
    sentences = text.split(". ")
    quiz = []

    for sentence in sentences[:3]:
        words = sentence.split()
        if len(words) < 6:
            continue

        answer = words[0]
        question = sentence.replace(answer, "______", 1)

        options = [answer]
        dummy = ["System", "Process", "Energy", "Structure"]
        options.extend(random.sample(dummy, 2))
        random.shuffle(options)

        correct_index = options.index(answer)

        quiz.append((question, options, correct_index))

    return quiz

# -------------------------------
# 💾 Session State
# -------------------------------
if "notes" not in st.session_state:
    st.session_state.notes = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

# -------------------------------
# 📥 Input
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
# 📚 Teach
# -------------------------------
if st.button("📚 Teach Me"):
    if selected_topic == "":
        st.warning("Please select a topic")
    else:
        st.session_state.notes = get_notes(selected_topic)

# -------------------------------
# 📘 Display
# -------------------------------
if st.session_state.notes:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📖 Explanation")
    st.write(st.session_state.notes)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔊 Listen Explanation"):
        speak(st.session_state.notes)

    # Images
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
    # 🧠 ADVANCED QUIZ
    # -------------------------------
    if st.button("🧠 Generate Quiz"):
        st.session_state.quiz = generate_advanced_quiz(st.session_state.notes)
        st.session_state.start_time = time.time()

    if st.session_state.quiz:
        st.subheader("🧠 Quiz Time")

        score = 0

        for i, (question, options, correct) in enumerate(st.session_state.quiz):
            answer = st.radio(f"Q{i+1}: {question}", options, key=f"quiz_{i}")

            if answer == options[correct]:
                score += 1

        if st.button("Submit Quiz"):
            end_time = time.time()
            total_time = int(end_time - st.session_state.start_time)

            st.success(f"Score: {score}/{len(st.session_state.quiz)}")
            st.info(f"Time Taken: {total_time} seconds")

# -------------------------------
# ❓ Doubt Section
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
# 🎉 Footer
# -------------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Personalized Learning Platform | Final Version
</p>
""", unsafe_allow_html=True)

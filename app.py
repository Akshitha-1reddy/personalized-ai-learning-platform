import streamlit as st
import wikipedia
from gtts import gTTS
import time

# 🎨 CSS Styling
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

# 🎓 Title
st.markdown("<h1>🎓 AI Personalized Learning Teacher</h1>", unsafe_allow_html=True)

# 📥 Input
topic = st.text_input("📘 Enter a Topic")

# 🎤 Voice Function (FIXED)
def speak(text):
    filename = f"voice_{int(time.time())}.mp3"
    tts = gTTS(text)
    tts.save(filename)

    with open(filename, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

# 📚 Wikipedia Fetch
def get_notes(topic):
    try:
        return wikipedia.summary(topic, sentences=5)
    
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=5)
    
    except:
        return f"""
        📘 {topic}

        This is an important topic.
        Please refer to textbooks for detailed explanation.
        """

# 💾 Session State
if "notes" not in st.session_state:
    st.session_state.notes = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

# 📚 Teach Button
if st.button("📚 Teach Me"):
    if topic == "":
        st.warning("⚠️ Please enter a topic")
    else:
        st.info("⏳ Fetching explanation...")
        st.session_state.notes = get_notes(topic)

# 📘 Show Notes
if st.session_state.notes:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📖 Lesson Explanation")
    st.write(st.session_state.notes)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔊 Listen Explanation"):
        speak(st.session_state.notes)

# ❓ Doubt Section
st.subheader("❓ Ask Your Doubt")

question = st.text_input("Type your question")

def get_answer(question):
    try:
        return wikipedia.summary(question, sentences=3)
    except:
        return "Please try asking in a simpler way."

# 💡 Answer Button
if st.button("💡 Get Answer"):
    if question == "":
        st.warning("⚠️ Please enter a question")
    else:
        st.session_state.answer = get_answer(question)

# 📗 Show Answer
if st.session_state.answer:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📗 Answer")
    st.write(st.session_state.answer)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔊 Listen Answer"):
        speak(st.session_state.answer)

# 🎉 Footer
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Made with ❤️ | Personalized Learning Platform
</p>
""", unsafe_allow_html=True)

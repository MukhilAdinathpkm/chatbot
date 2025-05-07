import streamlit as st
import google.generativeai as genai
import random
import time
from streamlit_lottie import st_lottie
import requests

# Configure Gemini API
genai.configure(api_key="AIzaSyA0M6LEI4uC4E13Xr8DwLWpuPbLNtTjffQ")  # Replace with your actual Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Custom prompt template for gym-specific queries
def get_workout_advice(prompt):
    system_prompt = f"""
You are a knowledgeable and experienced strength & conditioning coach who specializes in helping athletes and gym-goers optimize their physical performance.

Only respond with advice related to:
- muscle building strategies
- hypertrophy and strength training
- workout splits (push/pull, bro split, upper/lower)
- training periodization
- performance-enhancing techniques
- gym nutrition and recovery tips
- athletic training
- body conditioning
- diet
- improving specific skills required for athletics

Make your answer engaging, practical, and focused on gym performance.
Only answer what you are asked and dont give any extra information. When the user gives any appreciation message just say thank you and thats enough.
Dont always give advice for all the required domains.

User Question: {prompt}
"""
    try:
        response = model.generate_content(system_prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# App Configuration
st.set_page_config(page_title="🏋️‍♂️ HealthBot for Gym Rats", layout="wide", page_icon="💪")

# Load Lottie Animation
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_tutvdkg0.json"
lottie_json = load_lottie_url(lottie_url)

if lottie_json:
    st_lottie(lottie_json, height=250)
else:
    st.warning("⚠️ Could not load animation. Check the URL or your internet connection.")

# Sidebar Styling
with st.sidebar:
    st_lottie(lottie_json, height=250)
    st.title("💪 HealthBot Pro")
    st.markdown("""
    Ask me anything about:
    - 🏋️ Muscle building
    - 🧠 Workout science
    - 🍽️ Gym nutrition
    - 🧘 Recovery & injury prevention
    - 🔁 Training splits

    _Built with ❤️ for athletes and gym lovers._
    """)

# Main Title
st.markdown("<h1 style='text-align: center; color: white;'>🏋️ HealthBot – Your AI Gym Coach</h1>", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Ask your question about training, workouts, or performance...")

# Process input
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.spinner("Thinking like a coach..."):
        bot_reply = get_workout_advice(user_input)
    st.session_state.chat_history.append({"role": "bot", "text": bot_reply})

# Display conversation history
for i, chat in enumerate(st.session_state.chat_history):
    if chat["role"] == "user":
        with st.chat_message("user", avatar="image.png"):
            st.markdown(chat["text"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            if i == len(st.session_state.chat_history) - 1:
                # Animate only the latest bot response
                container = st.empty()
                displayed_text = ""
                for word in chat["text"].split():
                    displayed_text += word + " "
                    container.markdown(displayed_text)
                    time.sleep(0.03)
            else:
                st.markdown(chat["text"])

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ✅ MUST be first Streamlit command
st.set_page_config(page_title="SleepOptimizer", page_icon="💤")

# Custom CSS Theme
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .main {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
        }
        .stButton>button {
            background-color: #4b0082;
            color: white;
            border-radius: 10px;
            padding: 0.5em 2em;
        }
        .stButton>button:hover {
            background-color: #3a0066;
            color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load("model.pkl")

# UI
st.title("💤 SleepOptimizer")
st.markdown("**AI-powered sleep quality predictor with personalized suggestions.**")

st.sidebar.header("🧾 Your Daily Sleep Habits")

# Sidebar Inputs
age = st.sidebar.slider("Age", 10, 100, 25)
sleep_duration = st.sidebar.slider("Sleep Duration (hours)", 0.0, 12.0, 6.5)
physical_activity = st.sidebar.slider("Physical Activity Level (0–100)", 0, 100, 40)
stress_level = st.sidebar.slider("Stress Level (1–10)", 1, 10, 5)
heart_rate = st.sidebar.slider("Heart Rate (bpm)", 40, 120, 75)
bmi_category = st.sidebar.selectbox("BMI Category", ['Normal', 'Overweight', 'Obese'])
screen_time = st.sidebar.slider("Screen Time Before Bed (hours)", 0.0, 10.0, 3.0)
caffeine = st.sidebar.selectbox("Caffeine After 6 PM?", ['Yes', 'No'])

# Preprocess
def preprocess():
    bmi_map = {'Normal': 0, 'Overweight': 1, 'Obese': 2}
    caffeine_flag = 1 if caffeine == 'Yes' else 0
    return np.array([[age, sleep_duration, physical_activity, stress_level,
                      heart_rate, bmi_map[bmi_category], screen_time, caffeine_flag]])

X_input = preprocess()

# Predict
if st.button("🔍 Predict Sleep Quality"):
    prediction = model.predict(X_input)[0]
    st.success(f"🛏️ Your predicted sleep quality score: **{round(prediction, 2)} / 10**")

    st.subheader("💡 Tips to Improve Sleep")
    tips = []
    if sleep_duration < 7:
        tips.append("📌 Try to get at least 7–8 hours of sleep.")
    if stress_level > 6:
        tips.append("🧘 Reduce stress through meditation or light exercise.")
    if physical_activity < 40:
        tips.append("🏃 Increase daily activity for better rest.")
    if caffeine == 'Yes':
        tips.append("☕ Avoid caffeine after 6 PM.")
    if screen_time > 2:
        tips.append("📵 Reduce screen time before sleep.")

    if tips:
        for tip in tips:
            st.markdown(f"- {tip}")
    else:
        st.markdown("✅ Your habits are already sleep-friendly!")

st.markdown("---")
st.caption("Built with 💙 by Harshita Suri")

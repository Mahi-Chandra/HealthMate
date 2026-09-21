import streamlit as st
from datetime import datetime
from database import add_user, log_daily_data

st.set_page_config(page_title="HealthMate",layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.sidebar.title("🏥 HealthMate")

if st.session_state.user_id is None:
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    if st.sidebar.button("Login"):
        user_id = add_user(username,email)
        if user_id:
            st.session_state.user_id = user_id
            st.write("Logged in! ✅")
        else:
            st.error("Username already exists! Try a different one.")
            
if st.session_state.user_id:
    st.header("📝Daily Health Log")

    col1,col2,col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)",min_value = 30.0, max_value = 250.0)
        height = st.number_input("Height (cm)",min_value = 100, max_value = 250)

    with col2:
        water = st.number_input("Water (L)",min_value = 0, max_value = 4)
        steps = st.number_input("Steps",min_value=0, max_value= 50000)

    mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😞 Sad", "😤 Stressed"])
    with col3:
        calories = st.number_input("Calories eaten today", min_value=0, max_value=10000)

    if st.button("Save Log"):
        today = datetime.now().date()
        log_daily_data(st.session_state.user_id, today, weight, height, water, steps, mood, calories)
        st.success("Log saved! ✅")
else:
    st.title("🏥 Welcome to HEALTHMATE")
    st.info("Please login from the sidebar to get started")

# need to add features
    
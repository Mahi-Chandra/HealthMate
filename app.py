import streamlit as st
from datetime import datetime
import base64
from database import add_user, log_daily_data

def add_custom_css():
    st.markdown("""
    <style>
    /* Background with your image */
    [data-testid="stAppViewContainer"] {
        background-image: url('data:image/jpeg;base64,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');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .stMainBlockContainer {
        padding: 0;
        background: transparent !important;
    }
    
    .main {
        background: transparent !important;
    }

    
    /* Liquid glass effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 30px;
        padding: 80px 60px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2), 
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .app-title {
        color: #ffffff;
        font-size: 68px;
        font-weight: 400;
        font-family: "Lucida Console","Courier New",monospace;
        text-shadow: None;
        margin: 0;
        padding: 20px;
        letter-spacing: 1px;
        overflow: hidden;
        white-space: nowrap;
    }
    
    .app-subtitle {
        display: none;
    }
    
    /* Liquid glass buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
        padding: 12px 28px !important;
        font-size: 16px !important;
        font-weight: 600;
        font-family: "Lucida Console" !important;
        border-radius: 25px !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1)
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
    }
    /* Text inputs */
    *{
        font-family: "Lucida COnsole", "Courier New", !important;
    }
    
    /* All text */
    * {
        font-family: 'Outfit', sans-serif !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
add_custom_css()

st.set_page_config(page_title="HealthMate",layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.page == "landing" and not st.session_state.user_id:
    col1,col2 = st.columns([0.85,0.15])
    with col2:
        if st.button("🔐 Login", key="login_btn"):
            st.session_state.page="login"
            st.rerun()
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])
    with col2:
        st.markdown('''
        <div class = "glass-container">
            <div class = "app-title">HealthMate</div>
        </div>
        ''',unsafe_allow_html=True)

        st.write("")
        st.write("")

        col_a,col_b,col_c = st.columns([1,1.5,1])
        with col_b:
            if st.button("Get Started ->",key="cta_btn",use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

elif st.session_state.page == "login":
    col1,col2 = st.columns([0.85,0.15])
    with col2:
        if st.button("<- Back"):
            st.session_state.page = "landing"
            st.rerun()
    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])
    with col2:
        st.markdown("""
        <div class= "glass-container">
            <div class = "app-title">Login</div>
        </div>
        """,unsafe_allow_html=True)

        username = st.text_input("Username")
        email = st.text_input("Email")

        if st.button("Sign In",use_container_width=True):
            if username and email:
                user_id = add_user(username,email)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("A user with this username already exists! Please try a different one.")
            else:
                st.error("Please fill in all the fields")

elif st.session_state.page == "signup":
    col1,col2 = st.columns([0.85,0.15])
    with col2:
        if st.button("<-Back"):
            st.session_state.page = "landing"
            st.rerun()

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])
    with col2:
        st.markdown('''
        <div class= "glass-container">
            <div class = "app-title">Sign Up</div>
        </div>
        ''',unsafe_allow_html=True)

        username= st.text_input("Create Username")
        email = st.text_input("Enter your email")

        if st.button("Create an account",use_container_width=True):
            if username and email:
                user_id = add_user(username,email)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Username already exists! Try a different one.")
            else:
                st.error("Please fill in all fields")

elif st.session_state.page == "dashboard" and st.session_state.user_id:
    col1,col2 = st.columns([0.85,0.15])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.page = "landing"
            st.rerun()

    st.header(f"📝 Daily Health Log - {st.session_state.username}")

    col1,col2,col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)",min_value = 30.0, max_value = 250.0)
        height = st.number_input("Height (cm)",min_value = 100, max_value = 250)

    with col2:
        water = st.number_input("Water (ml)",min_value = 0, max_value = 4)
        steps = st.number_input("Steps",min_value=0, max_value= 50000)

    mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😞 Sad", "😤 Stressed"])
    with col3:
        calories = st.number_input("Calories eaten today", min_value=0, max_value=10000)

    if st.button("Save Log"):
        today = datetime.now().date()
        log_daily_data(st.session_state.user_id, today, weight, height, water, steps, mood, calories)
        st.success("Log saved! ✅")

 
    
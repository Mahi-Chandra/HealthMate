import streamlit as st
from datetime import datetime
import base64
import calendar as cal_module
import plotly.graph_objects as go
import os
import json
from database import (add_user, login_user, log_daily_data,
                      get_today_log, get_weekly_logs, get_recent_logs, get_month_log_dates)
from models import HealthAnalyzer
from config import HEALTH_ADVISORY_MESSAGES, HEALTH_DISCLAIMER, DAILY_WATER_INTAKE_GOAL, DAILY_STEP_GOAL

with open('bg.png', 'rb') as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

async def get_health_insights(weight, height, water, steps, mood, calories):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    bmi = round((weight / ((height / 100) ** 2)), 1)
    cal_burned = round(steps * 0.04)
    net_cal = calories - cal_burned
    
    prompt = f"""Based on this person's daily health data, provide 2-3 specific, actionable health insights:

Daily Data:
- Weight: {weight} kg
- Height: {height} cm (BMI: {bmi})
- Water intake: {water} ml (Goal: {DAILY_WATER_INTAKE_GOAL} ml)
- Steps: {steps:,} (Goal: {DAILY_STEP_GOAL:,})
- Calories eaten: {calories} (Burned from steps: {cal_burned})
- Net calories: {net_cal} kcal
- Mood: {mood}

Provide insights in a friendly, motivating tone. Focus on actionable advice. Keep it concise (2-3 sentences max)."""

    try:
        response = await st.session_state.async_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def add_custom_css():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #d4e4d0 0%, #c5dac0 25%, #b8d4c2 50%, #c9ddd0 75%, #dce8da 100%);
        background-size: cover;
        background-attachment: fixed;
    }
    
    .stMainBlockContainer {
        padding: 0;
        background: transparent !important;
    }
    
    .main {
        background: transparent !important;
    }

    .landing-content {
        text-align: center;
        position: relative;
        z-index: 10;
    }

    .hero-title {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 60px;
        font-weight: 300;
        color: rgba(15, 46, 36, 0.95);
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin: 0;
        padding: 0;
        letter-spacing: 1px;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 14px;
        color: rgba(15, 46, 36, 0.65);
        margin-top: 30px;
        letter-spacing: 1px;
        font-weight: 400;
    }

    .glass-container {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 80px 60px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        text-align: center;
    }
    
    .app-title {
        color: #0f2e24;
        font-size: 60px;
        font-weight: 400;
        font-family: "Lucida Console", "Courier New", monospace;
        margin: 0;
        padding: 20px;
        letter-spacing: 1px;
    }
    
    .app-subtitle {
        display: none;
    }
    
    .stButton > button {
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: #0f2e24 !important;
        padding: 12px 28px !important;
        font-size: 14px !important;
        font-weight: 600;
        font-family: "Lucida Console", "Courier New", monospace !important;
        border-radius: 25px !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }

    .form-title {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 22px;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.85);
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    .left-panel {
        background-image: url('data:image/jpeg;base64,SIDE_IMAGE_BASE64_HERE');
        background-size: cover;
        background-position: center;
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .left-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(8px);
    }

    .welcome-text {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 48px;
        font-weight: 350;
        color: rgba(255, 255, 255, 0.9);
        position: relative;
        z-index: 2;
        letter-spacing: 3px;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    .right-panel {
        background: transparent;
        padding: 60px 40px;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .form-container {
        width: 100%;
        max-width: 380px;
    }

    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    .stTextInput > div > div > input {
        font-family: "Lucida Console", "Courier New", monospace !important;
        border: none !important;
        background: transparent !important;
        color: #ffffff !important;
        font-size: 14px !important;
        padding: 10px 12px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    .stTextInput > div > div:focus-within {
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
    }

    .stTextInput label {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 12px !important;
    }

    * {
        font-family: "Lucida Console", "Courier New", monospace !important;
    }

    [data-testid="stColumns"] > div:first-child {
        background: #0f2e24;
        border-radius: 20px;
        padding: 16px 8px !important;
        min-height: 85vh;
    }

    [data-testid="stColumns"] > div:first-child .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        font-size: 12px !important;
        padding: 10px 8px !important;
        border-radius: 12px !important;
    }

    [data-testid="stColumns"] > div:first-child .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }

    .glass-card-sm {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    .nav-sidebar {
        text-align: center;
        padding: 8px 0;
    }

    .nav-logo {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 14px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        letter-spacing: 2px;
        margin-bottom: 20px;
        text-align: center;
    }

    .greeting-text {
        font-family: "Lucida Console", "Courier New", monospace;
        font-size: 24px;
        font-weight: 300;
        color: #1a1a1a;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    .top-bar-btn {
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        border-radius: 10px;
        padding: 10px 14px;
        color: #1a1a1a;
        font-size: 12px;
        text-align: center;
        margin-bottom: 8px;
    }

    .cal-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        color: #2c2c2c;
    }

    .cal-table th {
        color: #666;
        font-weight: 400;
        padding: 6px 2px;
        font-size: 10px;
        text-align: center;
    }

    .cal-table td {
        padding: 6px 2px;
        text-align: center;
        border-radius: 6px;
        font-size: 11px;
        color: #333;
    }

    .cal-today {
        background: #0f2e24;
        color: #ffffff !important;
        font-weight: 700;
        border-radius: 50%;
    }

    .cal-logged {
        background: rgba(100, 200, 100, 0.2);
        color: #1a5c2a !important;
        border-radius: 50%;
    }

    .cal-month-title {
        color: #1a1a1a;
        font-size: 14px;
        font-weight: 400;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    .streak-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-top: 2px;
    }
    .streak-green { background: #2e8b57; }
    .streak-red { background: #c0392b; }

    .calorie-header {
        font-size: 16px;
        color: #1a1a1a;
        margin-bottom: 12px;
    }

    .calorie-stat {
        font-size: 12px;
        color: #444;
        margin: 6px 0;
    }

    .calorie-net {
        font-size: 20px;
        font-weight: 600;
        margin-top: 8px;
    }

    .calorie-net.deficit { color: #2e8b57; }
    .calorie-net.surplus { color: #c0392b; }

    .progress-bar-bg {
        background: rgba(0, 0, 0, 0.08);
        border-radius: 10px;
        height: 8px;
        margin-top: 10px;
        overflow: hidden;
    }

    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    .tracker-title {
        font-size: 14px;
        color: #1a1a1a;
        margin-bottom: 12px;
    }

    .tracker-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }

    .tracker-label {
        font-size: 12px;
        color: #555;
    }

    .tracker-value {
        font-size: 14px;
        font-weight: 600;
        color: #1a1a1a;
    }

    .section-title {
        font-size: 16px;
        color: #1a1a1a;
        font-weight: 400;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .stNumberInput > div > div > input,
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
        color: #1a1a1a !important;
        font-size: 13px !important;
    }

    .stNumberInput > div > div,
    .stNumberInput > div {
        background: transparent !important;
        border-color: transparent !important;
    }

    .stNumberInput label {
        color: #333 !important;
        font-size: 12px !important;
    }

    .stNumberInput button,
    .stNumberInput [data-testid="stNumberInputStepUp"],
    .stNumberInput [data-testid="stNumberInputStepDown"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        color: #1a1a1a !important;
    }

    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
        color: #1a1a1a !important;
    }

    .stSelectbox label {
        color: #333 !important;
        font-size: 12px !important;
    }

    .stSelectbox > div > div > div,
    .stSelectbox [data-baseweb="select"] span {
        color: #1a1a1a !important;
    }

    [data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }

    [data-baseweb="base-input"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
    }

    [data-baseweb="select"] {
        background-color: transparent !important;
    }

    .analysis-card {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .analysis-title {
        font-size: 18px;
        font-weight: 400;
        color: #1a1a1a;
        margin-bottom: 16px;
        letter-spacing: 1px;
    }

    .advice-item {
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        color: #2c2c2c;
        font-size: 13px;
        line-height: 1.5;
    }

    .bmi-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .bmi-underweight { background: rgba(100, 180, 255, 0.2); color: #2a7ab5; }
    .bmi-normal { background: rgba(46, 139, 87, 0.2); color: #2e8b57; }
    .bmi-overweight { background: rgba(255, 165, 0, 0.2); color: #cc7a00; }
    .bmi-obese { background: rgba(192, 57, 43, 0.2); color: #c0392b; }

    .api-placeholder {
        background: rgba(255, 255, 255, 0.15);
        border: 1px dashed rgba(0, 0, 0, 0.15);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        color: #666;
        font-size: 13px;
    }

    .disclaimer-text {
        font-size: 10px;
        color: #888;
        margin-top: 12px;
        line-height: 1.4;
        font-style: italic;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    h1, h2, h3, h4 {
        color: #1a1a1a !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

add_custom_css()
st.set_page_config(page_title="HealthMate", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.page == "landing" and not st.session_state.user_id:
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        if st.button("login", key="login_btn"):
            st.session_state.page = "login"
            st.rerun()

    for _ in range(8):
        st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('''
        <div class="glass-container">
            <div class="hero-title">HealthMate</div>
            <div class="hero-subtitle">your personal health companion</div>
        </div>
        ''', unsafe_allow_html=True)

        st.write("")
        st.write("")

        col_a, col_b, col_c = st.columns([1, 1.5, 1])
        with col_b:
            if st.button("Get Started →", key="cta_btn", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

elif st.session_state.page == "login":
    left_col, right_col = st.columns(2, gap="small")
    
    with left_col:
        st.markdown('''
        <div class="left-panel" style="position: relative;">
            <div class="welcome-text">WELCOME</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with right_col:
        col_center = st.columns([1])[0]
        with col_center:
            st.markdown('<div class="form-title">Login</div>', unsafe_allow_html=True)
            st.write("")
            
            email = st.text_input("Email", key="login_email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            st.write("")
            
            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                if email and password:
                    user_id, username = login_user(email, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password!")
                else:
                    st.error("Please fill in all fields")
            
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back", use_container_width=True, key="login_back"):
                    st.session_state.page = "landing"
                    st.rerun()
            with col2:
                if st.button("Create account?", use_container_width=True, key="login_signup"):
                    st.session_state.page = "signup"
                    st.rerun()

elif st.session_state.page == "signup":
    left_col, right_col = st.columns(2, gap="small")
    
    with left_col:
        st.markdown('''
        <div class="left-panel" style="position: relative;">
            <div class="welcome-text">WELCOME</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with right_col:
        col_center = st.columns([1])[0]
        with col_center:
            st.markdown('<div class="form-title">Sign Up</div>', unsafe_allow_html=True)
            st.write("")
            
            username = st.text_input("Username", key="signup_username", placeholder="Create username")
            email = st.text_input("Email", key="signup_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="signup_password", placeholder="Create password")
            
            st.write("")
            
            if st.button("Create an Account", use_container_width=True, key="signup_btn"):
                if username and email and password:
                    user_id = add_user(username, email, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("Username already exists! Try a different one.")
                else:
                    st.error("Please fill in all fields")
            
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back", use_container_width=True, key="signup_back"):
                    st.session_state.page = "landing"
                    st.rerun()
            with col2:
                if st.button("Already have account?", use_container_width=True, key="signup_login"):
                    st.session_state.page = "login"
                    st.rerun()

elif st.session_state.page == "dashboard" and st.session_state.user_id:
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    today_log = get_today_log(st.session_state.user_id)
    weekly_logs = get_weekly_logs(st.session_state.user_id)
    recent_logs = get_recent_logs(st.session_state.user_id, 14)
    logged_dates = get_month_log_dates(st.session_state.user_id, now.year, now.month)

    nav_col, main_col, side_col = st.columns([0.8, 4, 2])

    with nav_col:
        st.markdown('''
        <div class="nav-sidebar">
            <div class="nav-logo">🩺<br>Health<br>Mate</div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("Dashboard", key="nav_dash", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("Analysis", key="nav_analysis", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()

        st.write("")
        st.write("")

        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.page = "landing"
            st.rerun()

    with main_col:
        st.markdown(f'''
        <div class="greeting-text">{greeting}, {st.session_state.username}</div>
        ''', unsafe_allow_html=True)
 
        st.markdown('<div class="section-title">Your Recent Activity</div>', unsafe_allow_html=True)

        if recent_logs:
            dates = [log["date"] for log in recent_logs]
            waters = [log["water"] or 0 for log in recent_logs]
            cals = [log["calories"] or 0 for log in recent_logs]
            steps_data = [log["steps"] or 0 for log in recent_logs]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=waters, name="💧 Water (ml)",
                line=dict(color="rgba(100, 180, 255, 0.9)", width=2),
                fill="tozeroy", fillcolor="rgba(100, 180, 255, 0.1)"
            ))
            fig.add_trace(go.Bar(
                x=dates, y=cals, name="🔥 Calories",
                marker_color="rgba(255, 150, 80, 0.6)",
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=steps_data, name="🚶 Steps",
                line=dict(color="rgba(100, 220, 150, 0.9)", width=2, dash="dot"),
                yaxis="y2"
            ))

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.05)",
                font=dict(family="Lucida Console, Courier New, monospace", color="rgba(255,255,255,0.7)", size=11),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                            font=dict(size=10, color="rgba(255,255,255,0.7)")),
                margin=dict(l=40, r=40, t=30, b=40),
                height=300,
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True),
                yaxis=dict(gridcolor="rgba(255,255,255,0.08)", showgrid=True, title=""),
                yaxis2=dict(overlaying="y", side="right", showgrid=False, title=""),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('''
            <div class="glass-card" style="text-align:center; padding:40px;">
                <div style="font-size:36px; margin-bottom:10px;">📊</div>
                <div style="color:rgba(255,255,255,0.6); font-size:13px;">
                    No data yet! Log your first day below to see your charts.
                </div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("---", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Log your health for today!</div>', unsafe_allow_html=True)

        log_c1, log_c2, log_c3 = st.columns(3)
        with log_c1:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, key="d_weight")
            height = st.number_input("Height (cm)", min_value=100, max_value=250, key="d_height")
        with log_c2:
            water = st.number_input("Water (ml)", min_value=0, max_value=4000, key="d_water")
            steps = st.number_input("Steps", min_value=0, max_value=50000, key="d_steps")
        with log_c3:
            mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😞 Sad", "😤 Stressed"], key="d_mood")
            calories = st.number_input("Calories eaten", min_value=0, max_value=10000, key="d_cal")

        if st.button("save log", use_container_width=True, key="save_log_btn"):
            today = datetime.now().date()
            log_daily_data(st.session_state.user_id, today, weight, height, water, steps, mood, calories)
            st.success("Log saved! ✅")
            st.rerun()

    with side_col:
        st.markdown(f'''
        <div class="top-bar-btn">{now.strftime("%a, %b %d")} • {now.strftime("%I:%M %p")}</div>
        <div class="top-bar-btn">{st.session_state.username}</div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        month_name = now.strftime("%B %Y")
        st.markdown(f'<div class="cal-month-title">📅 {month_name}</div>', unsafe_allow_html=True)

        cal = cal_module.Calendar(firstweekday=6)  
        month_days = cal.monthdayscalendar(now.year, now.month)
        today_day = now.day

        cal_html = '<table class="cal-table"><tr>'
        for day_name in ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]:
            cal_html += f'<th>{day_name}</th>'
        cal_html += '</tr>'

        for week in month_days:
            cal_html += '<tr>'
            for day in week:
                if day == 0:
                    cal_html += '<td></td>'
                elif day == today_day:
                    dot = '<br><span class="streak-dot streak-green"></span>' if day in logged_dates else ''
                    cal_html += f'<td class="cal-today">{day}{dot}</td>'
                elif day in logged_dates:
                    cal_html += f'<td class="cal-logged">{day}<br><span class="streak-dot streak-green"></span></td>'
                elif day < today_day:
                    cal_html += f'<td>{day}<br><span class="streak-dot streak-red"></span></td>'
                else:
                    cal_html += f'<td>{day}</td>'
            cal_html += '</tr>'
        cal_html += '</table>'

        st.markdown(cal_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        cal_eaten = 0
        cal_steps = 0
        if today_log:
            cal_eaten = today_log.get("calories", 0) or 0
            cal_steps = today_log.get("steps", 0) or 0

        cal_burned = round(cal_steps * 0.04)
        net_cal = cal_eaten - cal_burned
        net_class = "deficit" if net_cal <= 0 else "surplus"
        net_label = f"{abs(net_cal)} kcal {'deficit' if net_cal <= 0 else 'surplus'}"

        burn_pct = min(100, round((cal_burned / max(cal_eaten, 1)) * 100))
        bar_color = "#6fcf97" if net_cal <= 0 else "#f2994a"

        st.markdown(f'''
        <div class="glass-card">
            <div class="calorie-header">🔥 Calorie Burner</div>
            <div class="calorie-stat">🍽️ Eaten: <strong>{cal_eaten} kcal</strong></div>
            <div class="calorie-stat">🚶 Burned (from {cal_steps:,} steps): <strong>{cal_burned} kcal</strong></div>
            <div class="calorie-net {net_class}">{net_label}</div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {burn_pct}%; background: {bar_color};"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if weekly_logs:
            total_water = sum(log.get("water", 0) or 0 for log in weekly_logs)
            total_steps = sum(log.get("steps", 0) or 0 for log in weekly_logs)
            days_logged = len(weekly_logs)
            avg_water = round(total_water / max(days_logged, 1))
            avg_steps = round(total_steps / max(days_logged, 1))

            st.markdown(f'''
            <div class="glass-card">
                <div class="tracker-title">Weekly Tracker</div>
                <div class="tracker-row">
                    <span class="tracker-label">💧 Avg Water</span>
                    <span class="tracker-value">{avg_water} ml</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">🚶 Total Steps</span>
                    <span class="tracker-value">{total_steps:,}</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">🚶 Avg Steps/Day</span>
                    <span class="tracker-value">{avg_steps:,}</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">📋 Days Logged</span>
                    <span class="tracker-value">{days_logged}/7</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="glass-card">
                <div class="tracker-title">Weekly Tracker</div>
                <div style="color:rgba(255,255,255,0.5); font-size:12px; text-align:center; padding:10px;">
                    No data this week yet
                </div>
            </div>
            ''', unsafe_allow_html=True)

elif st.session_state.page == "analysis" and st.session_state.user_id:
    now = datetime.now()

    today_log = get_today_log(st.session_state.user_id)
    weekly_logs = get_weekly_logs(st.session_state.user_id)
    logged_dates = get_month_log_dates(st.session_state.user_id, now.year, now.month)

    nav_col, main_col, side_col = st.columns([0.8, 4, 2])

    with nav_col:
        st.markdown('''
        <div class="nav-sidebar">
            <div class="nav-logo">🩺<br>Health<br>Mate</div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button("Dashboard", key="a_nav_dash", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("Analysis", key="a_nav_analysis", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()

        st.write("")
        st.write("")

        if st.button("Logout", key="a_logout_btn", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.page = "landing"
            st.rerun()

    with main_col:
        st.markdown(f'''
        <div class="greeting-text">Today's Health Analysis</div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="analysis-card">
            <div class="analysis-title">🤖 AI Health Insights</div>
        ''', unsafe_allow_html=True)

        if today_log:
            weight = today_log.get("weight", 60) or 60
            height = today_log.get("height", 170) or 170
            water = today_log.get("water", 0) or 0
            steps = today_log.get("steps", 0) or 0
            mood_raw = today_log.get("mood", "neutral") or "neutral"
            calories = today_log.get("calories", 0) or 0

            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                st.markdown('''
                <div class="api-placeholder">
                    <div style="font-size:28px; margin-bottom:12px;">🔑</div>
                    <div>API Key not configured</div>
                    <div style="margin-top:8px; font-size:11px;">
                        Set ANTHROPIC_API_KEY environment variable to enable AI insights
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    bmi = round((weight / ((height / 100) ** 2)), 1)
                    cal_burned = round(steps * 0.04)
                    net_cal = calories - cal_burned
                    
                    prompt = f"""Based on this person's daily health data, provide 2-3 specific, actionable health insights:

Daily Data:
- Weight: {weight} kg
- Height: {height} cm (BMI: {bmi})
- Water intake: {water} ml (Goal: {DAILY_WATER_INTAKE_GOAL} ml)
- Steps: {steps:,} (Goal: {DAILY_STEP_GOAL:,})
- Calories eaten: {calories} (Burned from steps: {cal_burned})
- Net calories: {net_cal} kcal
- Mood: {mood_raw}

Provide insights in a friendly, motivating tone. Focus on actionable advice. Keep it concise (2-3 sentences max)."""

                    message = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=300,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    insight = message.content[0].text
                    st.markdown(f'<div class="advice-item">💡 {insight}</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'''
                    <div class="api-placeholder">
                        <div>⚠️ API Error</div>
                        <div style="margin-top:8px; font-size:11px;">
                            {str(e)}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="api-placeholder">
                <div style="font-size:28px; margin-bottom:12px;">📝</div>
                <div>Log today's data on Dashboard first</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('''
        <div class="analysis-card">
            <div class="analysis-title">Health Advisory</div>
        ''', unsafe_allow_html=True)

        if today_log:
            weight = today_log.get("weight", 60) or 60
            height = today_log.get("height", 170) or 170
            water = today_log.get("water", 0) or 0
            steps = today_log.get("steps", 0) or 0
            mood_raw = today_log.get("mood", "neutral") or "neutral"
            mood_text = mood_raw.split(" ")[-1] if " " in mood_raw else mood_raw

            analyzer = HealthAnalyzer(weight, height, water, steps, mood_text)
            bmi = round(analyzer.calculate_bmi(), 1)
            category = analyzer.get_bmi_category()
            advice_list = analyzer.generate_advisory()

            bmi_class = category.lower()
            if bmi_class not in ("underweight", "normal", "overweight", "obese"):
                bmi_class = "normal"

            st.markdown(f'''
            <div style="margin-bottom:16px;">
                <span style="color:rgba(255,255,255,0.7); font-size:13px;">Your BMI:</span>
                <span style="color:#ffffff; font-size:22px; font-weight:600; margin-left:8px;">{bmi}</span>
                <span class="bmi-badge bmi-{bmi_class}">{category}</span>
            </div>
            ''', unsafe_allow_html=True)

            water_pct = min(100, round((water / DAILY_WATER_INTAKE_GOAL) * 100))
            steps_pct = min(100, round((steps / DAILY_STEP_GOAL) * 100))

            st.markdown(f'''
            <div style="margin-bottom:12px;">
                <span style="color:rgba(255,255,255,0.7); font-size:12px;">💧 Water: {water}ml / {DAILY_WATER_INTAKE_GOAL}ml ({water_pct}%)</span>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width:{water_pct}%; background:#64b4ff;"></div>
                </div>
            </div>
            <div style="margin-bottom:16px;">
                <span style="color:rgba(255,255,255,0.7); font-size:12px;">🚶 Steps: {steps:,} / {DAILY_STEP_GOAL:,} ({steps_pct}%)</span>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width:{steps_pct}%; background:#6fcf97;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            for advice in advice_list:
                st.markdown(f'<div class="advice-item">💡 {advice}</div>', unsafe_allow_html=True)

            cat_key = category.lower()
            if cat_key in HEALTH_ADVISORY_MESSAGES:
                st.markdown(f'<div class="advice-item">📌 {HEALTH_ADVISORY_MESSAGES[cat_key]}</div>', unsafe_allow_html=True)
            if water < DAILY_WATER_INTAKE_GOAL and "low_water_intake" in HEALTH_ADVISORY_MESSAGES:
                st.markdown(f'<div class="advice-item">💧 {HEALTH_ADVISORY_MESSAGES["low_water_intake"]}</div>', unsafe_allow_html=True)
            if steps < DAILY_STEP_GOAL and "low_steps" in HEALTH_ADVISORY_MESSAGES:
                st.markdown(f'<div class="advice-item">🚶 {HEALTH_ADVISORY_MESSAGES["low_steps"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="advice-item">😊 Mood: {mood_raw} — {analyzer.check_mood()}</div>', unsafe_allow_html=True)

        else:
            st.markdown('''
            <div style="text-align:center; padding:20px; color:rgba(255,255,255,0.5); font-size:13px;">
                <div style="font-size:28px; margin-bottom:10px;">📝</div>
                Log today's data on the Dashboard first to see your health analysis.
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="disclaimer-text">⚠️ {HEALTH_DISCLAIMER}</div>
        ''', unsafe_allow_html=True)

    with side_col:
        st.markdown(f'''
        <div class="top-bar-btn">{now.strftime("%a, %b %d")} • {now.strftime("%I:%M %p")}</div>
        <div class="top-bar-btn">{st.session_state.username}</div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        month_name = now.strftime("%B %Y")
        st.markdown(f'<div class="cal-month-title">📅 {month_name}</div>', unsafe_allow_html=True)

        cal = cal_module.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(now.year, now.month)
        today_day = now.day

        cal_html = '<table class="cal-table"><tr>'
        for day_name in ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]:
            cal_html += f'<th>{day_name}</th>'
        cal_html += '</tr>'

        for week in month_days:
            cal_html += '<tr>'
            for day in week:
                if day == 0:
                    cal_html += '<td></td>'
                elif day == today_day:
                    dot = '<br><span class="streak-dot streak-green"></span>' if day in logged_dates else ''
                    cal_html += f'<td class="cal-today">{day}{dot}</td>'
                elif day in logged_dates:
                    cal_html += f'<td class="cal-logged">{day}<br><span class="streak-dot streak-green"></span></td>'
                elif day < today_day:
                    cal_html += f'<td>{day}<br><span class="streak-dot streak-red"></span></td>'
                else:
                    cal_html += f'<td>{day}</td>'
            cal_html += '</tr>'
        cal_html += '</table>'

        st.markdown(cal_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        cal_eaten = 0
        cal_steps = 0
        if today_log:
            cal_eaten = today_log.get("calories", 0) or 0
            cal_steps = today_log.get("steps", 0) or 0

        cal_burned = round(cal_steps * 0.04)
        net_cal = cal_eaten - cal_burned
        net_class = "deficit" if net_cal <= 0 else "surplus"
        net_label = f"{abs(net_cal)} kcal {'deficit' if net_cal <= 0 else 'surplus'}"
        burn_pct = min(100, round((cal_burned / max(cal_eaten, 1)) * 100))
        bar_color = "#6fcf97" if net_cal <= 0 else "#f2994a"

        st.markdown(f'''
        <div class="glass-card">
            <div class="calorie-header">🔥 Calorie Burner</div>
            <div class="calorie-stat">🍽️ Eaten: <strong>{cal_eaten} kcal</strong></div>
            <div class="calorie-stat">🚶 Burned (from {cal_steps:,} steps): <strong>{cal_burned} kcal</strong></div>
            <div class="calorie-net {net_class}">{net_label}</div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {burn_pct}%; background: {bar_color};"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if weekly_logs:
            total_water = sum(log.get("water", 0) or 0 for log in weekly_logs)
            total_steps = sum(log.get("steps", 0) or 0 for log in weekly_logs)
            days_logged = len(weekly_logs)
            avg_water = round(total_water / max(days_logged, 1))
            avg_steps = round(total_steps / max(days_logged, 1))

            st.markdown(f'''
            <div class="glass-card">
                <div class="tracker-title">📊 Weekly Tracker</div>
                <div class="tracker-row">
                    <span class="tracker-label">💧 Avg Water</span>
                    <span class="tracker-value">{avg_water} ml</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">🚶 Total Steps</span>
                    <span class="tracker-value">{total_steps:,}</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">🚶 Avg Steps/Day</span>
                    <span class="tracker-value">{avg_steps:,}</span>
                </div>
                <div class="tracker-row">
                    <span class="tracker-label">📋 Days Logged</span>
                    <span class="tracker-value">{days_logged}/7</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="glass-card">
                <div class="tracker-title">📊 Weekly Tracker</div>
                <div style="color:rgba(255,255,255,0.5); font-size:12px; text-align:center; padding:10px;">
                    No data this week yet
                </div>
            </div>
            ''', unsafe_allow_html=True)

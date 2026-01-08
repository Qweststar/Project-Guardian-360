import streamlit as st
import datetime
import random
import requests
import urllib.parse
from streamlit_autorefresh import st_autorefresh

# --- DASHBOARD CONTROL ---
st.sidebar.title("🛡️ Guardian 360")
pause_wisdom = st.sidebar.toggle("Pause Wisdom Timer", value=False)

if not pause_wisdom:
    st_autorefresh(interval=10000, key="wisdom_refresh")

# --- FIXED WISDOM ENGINE ---
def fetch_zen_wisdom():
    # Pre-defined fallbacks to prevent "NoneType" errors
    fallbacks = [
        ("“Consistency is the highest form of love.”", "— Guardian Principle"),
        ("“I am the calm in my child's storm.”", "— Parent Affirmation"),
        ("“The way we talk to our children becomes their inner voice.”", "— Peggy O'Mara")
    ]
    try:
        url = f"https://zenquotes.io/api/random?cb={random.randint(1, 100000)}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return str(data[0]['q']), f"— {data[0]['a']}"
    except Exception:
        pass
    return random.choice(fallbacks) # Guaranteed to return two strings

# --- THE ADVISOR ENGINE ---
def get_advisor_guidance(query):
    query = query.lower().strip()
    # Logic to identify broad questions vs specific behaviors
    if any(word in query for word in ["partner", "marriage", "relationship", "how to be", "better"]):
        steps = [
            "Practice Active Listening: Dedicate 15 minutes daily to distraction-free talk.",
            "The 5:1 Ratio: Focus on 5 positive interactions for every 1 conflict.",
            "Unified Front: Discuss family boundaries privately before enforcing them."
        ]
        yt_query = urllib.parse.quote(f"{query} seminars expert advice")
        return steps, f"https://www.youtube.com/results?search_query={yt_query}"
    return None, None

# --- THEME & STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #DDB892 !important; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #6B4423 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: 700 !important; }
    h1, h2, h3, h4 { color: #000000 !important; font-weight: 800 !important; }
    .wisdom-vault {
        background-color: #EDE0D4 !important; padding: 25px; border-radius: 15px;
        border-left: 12px solid #6B4423; display: flex; align-items: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15); margin-bottom: 20px;
    }
    .stRadio { background-color: #6B4423 !important; padding: 20px; border-radius: 12px; border: 2px solid #4B3832; }
    .stRadio label { color: #FFFFFF !important; }
    .stTextInput input { background-color: #F5EBE0 !important; color: #000000 !important; border: 2px solid #6B4423 !important; font-weight: 700 !important; }
    .step-card { background: #EDE0D4; border-radius: 15px; padding: 20px; border: 2px solid #7F5539; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- UI ---
st.title("Guardian Response Partner")

# FETCH WISDOM (Error-checked)
quote_data = fetch_zen_wisdom()
quote, author = quote_data

st.markdown(f"""
    <div class="wisdom-vault">
        <div style="font-size:50px; margin-right:25px;">🛡️</div>
        <div>
            <p style="font-size:1.25rem; font-weight:800; font-style:italic; margin:0;">{quote}</p>
            <p style="font-weight:600; margin-top:5px;">{author}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.button("For Wisdom"):
    st.rerun()

st.divider()

age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What is on your heart?", placeholder="Ask a question or report a behavior...")

if user_input:
    advice_steps, yt_link = get_advisor_guidance(user_input)
    
    if advice_steps:
        st.markdown(f"### Guidance for: *{user_input}*")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{advice_steps[0]}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{advice_steps[1]}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{advice_steps[2]}</p></div>', unsafe_allow_html=True)
        st.link_button("🎥 Watch Expert Seminars on this Topic", yt_link)
    else:
        # Behavioral Logic Fallback
        res = [f"Gentle redirection for {user_input}", f"Firm boundary for {user_input}", f"Direct Line for {user_input}"]
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{res[0]}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{res[1]}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{res[2]}</p></div>', unsafe_allow_html=True)

st.markdown("<br><h4 style='text-align: center;'>✨ I am the calm in my child's storm. ✨</h4>", unsafe_allow_html=True)

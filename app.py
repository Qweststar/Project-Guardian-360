import streamlit as st
import datetime
import random
import requests
from streamlit_autorefresh import st_autorefresh

# --- DASHBOARD CONTROL ---
st.sidebar.title("🛡️ Guardian 360")
pause_wisdom = st.sidebar.toggle("Pause Wisdom Timer", value=False)

# --- 10-SECOND AUTO-REFRESH TIMER ---
# Only runs if the toggle is NOT checked
if not pause_wisdom:
    st_autorefresh(interval=10000, key="wisdom_refresh")

# --- LIVE WISDOM ENGINE ---
def fetch_zen_wisdom():
    try:
        # Cache-buster forces a fresh pull from the ZenQuotes API
        url = f"https://zenquotes.io/api/random?cb={random.randint(1, 100000)}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"“{data[0]['q']}”", f"— {data[0]['a']}"
    except:
        pass
    
    # Robust Fallback List
    fallbacks = [
        ("“Consistency is the highest form of love.”", "— Guardian Principle"),
        ("“I am the calm in my child's storm.”", "— Parent Affirmation"),
        ("“Firmness and Grace are the two wings of the Guardian.”", "— Mentorship Core")
    ]
    return random.choice(fallbacks)

# --- THEME & INTERFACE STYLING ---
st.markdown("""
    <style>
    /* Autumn Tan Background & Pure Black Text */
    .stApp { background-color: #DDB892 !important; color: #000000 !important; }
    
    /* Sidebar: Deep Earthy Brown-Red */
    [data-testid="stSidebar"] { background-color: #6B4423 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: 700 !important; }
    
    /* Headers & Text Formatting */
    h1, h2, h3, h4 { color: #000000 !important; font-weight: 800 !important; }

    /* THE WISDOM VAULT - Solid High-Contrast Styling */
    .wisdom-vault {
        background-color: #EDE0D4 !important; 
        padding: 25px;
        border-radius: 15px;
        border-left: 12px solid #6B4423; 
        display: flex;
        align-items: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    .mentor-avatar {
        font-size: 50px;
        margin-right: 25px;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
    }
    .wisdom-content { color: #000000 !important; }
    .quote-text { font-size: 1.25rem; font-weight: 800; font-style: italic; line-height: 1.4; margin: 0; }
    .author-text { font-size: 1rem; font-weight: 600; margin-top: 5px; opacity: 0.8; }

    /* Radio/Input Styling (Deep Earthy Brown-Red) */
    .stRadio { background-color: #6B4423 !important; padding: 20px; border-radius: 12px; border: 2px solid #4B3832; }
    .stRadio label { color: #FFFFFF !important; }
    
    /* Input Field Visibility */
    .stTextInput input { 
        background-color: #F5EBE0 !important; 
        color: #000000 !important; 
        border: 2px solid #6B4423 !important; 
        font-weight: 700 !important;
    }
    
    /* Response Cards */
    .step-card {
        background: #EDE0D4; 
        border-radius: 15px; 
        padding: 20px;
        border: 2px solid #7F5539; 
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_state = st.sidebar.select_slider("Child's State", options=["Calm", "Tired", "Stressed", "Meltdown"])

# --- MAIN DASHBOARD ---
st.title("Guardian Response Partner")

# FETCH AND DISPLAY WISDOM
quote, author = fetch_zen_wisdom()

st.markdown(f"""
    <div class="wisdom-vault">
        <div class="mentor-avatar">🛡️</div>
        <div class="wisdom-content">
            <p class="quote-text">{quote}</p>
            <p class="author-text">{author}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# MANUAL REFRESH BUTTON
if st.button("For Wisdom"):
    st.rerun()

if grace_state == "Meltdown":
    st.info("✨ **Grace Note:** Connection first. Focus only on Step 1 right now.")

st.divider()

# AGE SELECTION & INPUT
age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What's on your heart? (Type and press Enter)", placeholder="e.g., They are being disrespectful...")

# --- RESPONSE LOGIC ---
def get_responses(text, age_val):
    val = text.lower().strip()
    # Logic remains consistent with the tiered system requested
    child_map = {
        "hit": ["Let's use helping hands.", "No hitting. If it happens again, playtime ends.", "You chose to hit. We are pausing now to calm down."],
        "lying": ["I'm ready for the truth.", "I can only help when you are honest.", "Trust is broken. We're pausing until we repair it."],
        "running": ["I'd love to see you walk inside.", "Walking feet only. If you run again, let's take a reset.", "Since safety is hard now, we're pausing this activity."]
    }
    teen_map = {
        "late": ["Let's be mindful of time.", "Being late is a safety issue. Trust needs a reset.", "Curfew broken. Staying home next weekend to rebuild trust."],
        "disrespect": ["Please use a respectful tone.", "I'll listen when you are calm. Disrespect ends the talk.", "Respect is required. [Privilege] suspended until we talk properly."],
        "phone": ["Let's put the phones away for dinner.", "The rule is no phones at the table. Basket, please.", "I'll hold the phone until morning to help you reset."]
    }
    
    lib = teen_map if age_val == "Teen" else child_map
    for k, v in lib.items():
        if k in val: return v
    return [f"Step 1 for {text}", f"Step 2 for {text}", f"Direct Line for {text}"]

if user_input:
    res = get_responses(user_input, age)
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{res[0]}</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{res[1]}</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{res[2]}</p></div>', unsafe_allow_html=True)
    
    if st.button("📝 Record Progress"):
        st.success(f"Great work maintaining the line with {partner_name}. 🌿")

# BOTTOM AFFIRMATION (Static for grounding)
st.markdown("<br><h4 style='text-align: center;'>✨ I am the calm in my child's storm. ✨</h4>", unsafe_allow_html=True)

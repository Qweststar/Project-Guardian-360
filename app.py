import streamlit as st
import datetime
import random
import requests
from streamlit_autorefresh import st_autorefresh

# --- 10-SECOND AUTO-REFRESH TIMER ---
# This refreshes the app every 10,000 milliseconds (10 seconds)
count = st_autorefresh(interval=10000, key="wisdom_timer")

# --- LIVE WISDOM ENGINE ---
def get_guardian_wisdom():
    try:
        # ZenQuotes API - Pulls a fresh quote on every refresh
        response = requests.get("https://zenquotes.io/api/random", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return f"“{data[0]['q']}” — {data[0]['a']}"
    except:
        fallbacks = [
            "“Consistency is the highest form of love.”",
            "“I am the calm in my child's storm.”",
            "“Firmness and Grace are the two wings of the Guardian.”"
        ]
        return random.choice(fallbacks)

# --- FORCED SUNSET EARTH & PURE BLACK TEXT THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #DDB892 !important; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #6B4423 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important; font-weight: 700 !important;
    }
    h1, h2, h3, h4 { color: #000000 !important; font-family: 'Inter', sans-serif; font-weight: 800 !important; }
    
    /* Selection Box (Deep Earthy Brown-Red) */
    .stRadio { background-color: #6B4423 !important; padding: 15px; border-radius: 12px; border: 2px solid #4B3832; }
    .stRadio label { color: #FFFFFF !important; font-weight: 700 !important; }
    
    .step-card {
        background: #EDE0D4; border-radius: 15px; padding: 20px;
        border: 2px solid #7F5539; margin-bottom: 20px;
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .wisdom-box {
        background-color: rgba(107, 68, 35, 0.1);
        padding: 20px; border-radius: 12px;
        text-align: center; border-left: 8px solid #6B4423;
        font-style: italic; font-weight: 600; margin-bottom: 25px;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def get_tiered_responses(user_input, age_group):
    # Python is case sensitive, so we ensure input is handled consistently
    lookup = user_input.lower().strip()
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Safety Alert.** Please pause. Reach out to 988 for crisis support."

    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, let's take a reset break.", "Since safety is hard right now, we’re pausing this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, the play session ends.", "You chose to hit. Playtime is over while we calm down."],
        "lying": ["It feels like there's more to the story. I'm ready for the truth.", "I can only help you when I know what really happened.", "Trust is the anchor. Because of the dishonesty, we're pausing until we repair it."],
        "disrespect": ["I hear your frustration, but let's try a more respectful tone.", "I'm here to listen when you use a calm voice.", "I value our relationship too much for this tone. We'll talk again when you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Could we put the phones away so we can enjoy dinner together?", "The rule is no phones at the table. Please put it in the basket.", "I'll hold onto the phone until morning to help you reset."],
        "room": ["I noticed the room needs some attention. Need a hand?", "The room needs to be clean by 6 PM to go out tonight.", "The room isn't ready. Plans for tonight are on hold until the job is done."],
        "late": ["I noticed you were a bit late. Let's be mindful next time.", "Being late is a safety concern. We need to reset our trust.", "Curfew was broken. We'll stay home next weekend to rebuild trust."],
        "lying": ["I'm giving you a safe space to be honest right now.", "Lying makes the situation heavier. Let's fix this now.", "Trust is broken. Privilege is suspended while we rebuild your word."],
        "disrespect": ["I hear your frustration, but please communicate that respectfully.", "We can disagree, but you must remain respectful.", "Respect is required. [Privilege] is suspended until we can talk properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup: return responses, None
            
    return [f"Gentle redirection for '{user_input}'.", f"Firm expectation for '{user_input}'.", f"Direct Line consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---
st.sidebar.title("🛡️ Guardian 360")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("Child's State", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Response Partner")

# WISDOM BOX WITH AUTO-TIMER
st.markdown(f'<div class="wisdom-box">{get_guardian_wisdom()}</div>', unsafe_allow_html=True)

if st.button("Now let me give you a new perspective"):
    st.rerun()

if grace_context == "Meltdown":
    st.info("✨ **Grace Note:** Connection first. Focus only on Step 1 right now.")

st.divider()

age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What's on your heart?", placeholder="Type here...")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{responses[0]}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{responses[1]}</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{responses[2]}</p></div>', unsafe_allow_html=True)
        
        if st.button("📝 Record Progress"):
            st.success(f"Great work maintaining the line with {partner_name}. 🌿")

# BOTTOM AFFIRMATION (Also rotates every 10s)
affirmations = ["I am the calm in my child's storm.", "Consistency is the highest form of love.", "I have the strength to be firm and the heart to be gracious."]
st.markdown(f"<h4 style='text-align: center; margin-top: 50px;'>✨ {random.choice(affirmations)} ✨</h4>", unsafe_allow_html=True)

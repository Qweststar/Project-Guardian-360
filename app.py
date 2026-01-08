import streamlit as st
import datetime
import random
import requests
from streamlit_autorefresh import st_autorefresh

# --- 10-SECOND AUTO-REFRESH TIMER ---
st_autorefresh(interval=10000, key="wisdom_timer")

# --- LIVE WISDOM ENGINE (With Cache Bypassing) ---
def get_guardian_wisdom():
    try:
        # Adding a random parameter to the URL to force a fresh pull from the API
        response = requests.get(f"https://zenquotes.io/api/random?cb={random.randint(1,1000)}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"“{data[0]['q']}” — {data[0]['a']}"
    except:
        fallbacks = [
            "“Consistency is the highest form of love.”",
            "“I am the calm in my child's storm.”",
            "“The way we talk to our children becomes their inner voice.”"
        ]
        return random.choice(fallbacks)

# --- FORCED AUTUMN EARTH & PURE BLACK TEXT THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #DDB892 !important; color: #000000 !important; }
    
    [data-testid="stSidebar"] { background-color: #6B4423 !important; }
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

    /* FIXED WISDOM BOX - Solid Background, No Fade, with Avatar Space */
    .wisdom-container {
        display: flex;
        align-items: center;
        background-color: #EDE0D4 !important; /* Solid background to stop fading */
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #6B4423;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .avatar-icon {
        font-size: 40px;
        margin-right: 20px;
    }
    .wisdom-text {
        font-style: italic;
        font-weight: 700;
        color: #000000 !important;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def get_tiered_responses(user_input, age_group):
    # Python is case sensitive; we use .lower() for reliability
    lookup = user_input.lower().strip()
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Safety Alert.** Please pause. Reach out to 988 if things feel unsafe."

    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, let's take a reset break.", "Since safety is hard right now, we’re pausing this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, playtime ends.", "You chose to hit. Playtime is over while we calm down."],
        "lying": ["It feels like there's more to the story. I'm ready for the truth.", "I can only help you when I know what really happened.", "Trust is the anchor. Because of the dishonesty, we're pausing until we repair it."],
        "disrespect": ["I hear your frustration, but let's try a more respectful tone.", "I'm here to listen when you use a calm voice.", "I value our relationship too much for this tone. We'll talk when you can lead with respect."]
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

# WISDOM BOX WITH AVATAR & AUTO-TIMER
current_wisdom = get_guardian_wisdom()
st.markdown(f"""
    <div class="wisdom-container">
        <div class="avatar-icon">🛡️</div>
        <div class="wisdom-text">{current_wisdom}</div>
    </div>
    """, unsafe_allow_html=True)

if st.button("For Wisdom"):
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

# BOTTOM AFFIRMATION
affirmations = ["I am the calm in my child's storm.", "Consistency is the highest form of love.", "Firmness and Grace are my strengths."]
st.markdown(f"<h4 style='text-align: center; margin-top: 50px;'>✨ {random.choice(affirmations)} ✨</h4>", unsafe_allow_html=True)

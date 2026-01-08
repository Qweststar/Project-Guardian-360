import streamlit as st
import datetime
import random
import requests
from streamlit_autorefresh import st_autorefresh

# --- DASHBOARD CONTROL ---
st.sidebar.title("🛡️ Guardian 360")
pause_wisdom = st.sidebar.toggle("Pause Wisdom Timer", value=False)

if not pause_wisdom:
    st_autorefresh(interval=10000, key="wisdom_refresh")

# --- LIVE WISDOM ENGINE ---
def fetch_zen_wisdom():
    try:
        url = f"https://zenquotes.io/api/random?cb={random.randint(1, 100000)}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"“{data[0]['q']}”", f"— {data[0]['a']}"
    except:
        return ("“Consistency is the highest form of love.”", "— Guardian Principle")

# --- THE ADVISOR ENGINE (New Capability) ---
def get_advisor_guidance(query):
    query = query.lower().strip()
    
    # Example: How to be a better partner
    if "partner" in query or "marriage" in query:
        steps = [
            "Practice Active Listening: Dedicate 15 minutes daily to distraction-free talk.",
            "The 5:1 Ratio: Ensure you have 5 positive interactions for every 1 conflict.",
            "Establish the 'Unified Front': Discuss boundaries privately before enforcing them together."
        ]
        resources = "[The Gottman Institute](https://www.gottman.com) | [Greater Good Magazine](https://greatergood.berkeley.edu)"
        return steps, resources

    # Example: Handling Stress/Patience
    elif "patience" in query or "better parent" in query:
        steps = [
            "Self-Regulation: Take 3 deep breaths before responding to a trigger.",
            "Reframing: See the behavior as a 'call for help' rather than 'defiance'.",
            "Repair: If you lose your cool, apologize and explain your feelings to the child."
        ]
        resources = "[Positive Discipline](https://www.positivediscipline.com) | [Aha! Parenting](https://www.ahaparenting.com)"
        return steps, resources

    return None, None

# --- THEME & INTERFACE STYLING ---
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
    .mentor-avatar { font-size: 50px; margin-right: 25px; }
    .stRadio { background-color: #6B4423 !important; padding: 20px; border-radius: 12px; border: 2px solid #4B3832; }
    .stRadio label { color: #FFFFFF !important; }
    .stTextInput input { background-color: #F5EBE0 !important; color: #000000 !important; border: 2px solid #6B4423 !important; font-weight: 700 !important; }
    .step-card { background: #EDE0D4; border-radius: 15px; padding: 20px; border: 2px solid #7F5539; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- UI ---
st.title("Guardian Response Partner")
quote, author = fetch_zen_wisdom()
st.markdown(f'<div class="wisdom-vault"><div class="mentor-avatar">🛡️</div><div class="wisdom-content"><p style="font-size:1.25rem; font-weight:800; font-style:italic;">{quote}</p><p style="font-weight:600;">{author}</p></div></div>', unsafe_allow_html=True)

if st.button("For Wisdom"):
    st.rerun()

st.divider()

age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What is on your heart or what do you need advice on?", placeholder="e.g., How do I become a better partner?")

if user_input:
    # Check if it's a general advice question
    advice_steps, resources = get_advisor_guidance(user_input)
    
    if advice_steps:
        st.markdown(f"### Guidance for: *{user_input}*")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{advice_steps[0]}</p></div>', unsafe_allow_html=True)
        with col2: # Fixed from c2 to col2 if using standard column naming, but keeping c2 for your code consistency
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{advice_steps[1]}</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{advice_steps[2]}</p></div>', unsafe_allow_html=True)
        st.info(f"📚 **Recommended Resources:** {resources}")
    else:
        # Behavioral Logic
        child_map = {"hit": ["Helping hands.", "No hitting.", "Play pause."], "lying": ["Tell the truth.", "I need honesty.", "Repairing trust."]}
        teen_map = {"late": ["Check the time.", "Safety concern.", "Curfew reset."], "disrespect": ["Tone check.", "Listen when calm.", "Respect required."]}
        lib = teen_map if age == "Teen" else child_map
        res = [f"Step 1 for {user_input}", f"Step 2 for {user_input}", f"Direct Line for {user_input}"]
        for k, v in lib.items():
            if k in user_input.lower(): res = v
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h4>Step 1</h4><p>{res[0]}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h4>Step 2</h4><p>{res[1]}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h4>Direct Line</h4><p>{res[2]}</p></div>', unsafe_allow_html=True)

st.markdown("<br><h4 style='text-align: center;'>✨ I am the calm in my child's storm. ✨</h4>", unsafe_allow_html=True)

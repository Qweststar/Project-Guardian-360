import streamlit as st
import datetime
import random
import requests
import urllib.parse
from streamlit_autorefresh import st_autorefresh

# --- 10-SECOND AUTO-REFRESH TIMER ---
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
        return ("“Integrity is doing the right thing, even when no one is watching.”", "— C.S. Lewis")

# --- UNIVERSAL ADVISOR ENGINE (Adult & Relationship Focused) ---
def get_universal_guidance(query, user_type):
    query = query.lower().strip()
    
    # CASE: Co-Parenting Accountability
    if any(word in query for word in ["co-parent", "ex-wife", "ex-husband", "exchange"]):
        steps = [
            "Parallel Parenting: Keep communication strictly about logistics (times, dates, health). Avoid emotional baiting.",
            "The Business Model: Treat interactions like a professional business meeting. Be polite, concise, and clear.",
            "Direct Line: If boundaries are crossed, revert to the written parenting plan immediately. Do not engage in side arguments."
        ]
        yt_search = "co-parenting with a high conflict person psychology"
        return steps, "BIFF Method | Parallel Parenting Research", yt_search

    # CASE: Partnership / Marriage Strength
    elif any(word in query for word in ["partner", "marriage", "wife", "husband"]):
        steps = [
            "Soft Start-up: Bring up concerns without blame. Use 'I feel' statements instead of 'You always' statements.",
            "Accountability: Take 100% responsibility for your 50% of the conflict. Acknowledge your triggers openly.",
            "Direct Line: When tensions rise, call a 20-minute 'Positive Timeout' to calm your nervous systems before speaking again."
        ]
        yt_search = "Gottman relationship repair and accountability"
        return steps, "Gottman Institute | Seven Principles for Making Marriage Work", yt_search

    # CASE: Single Parenting / Self-Growth
    elif any(word in query for word in ["single parent", "lonely", "exhausted", "myself"]):
        steps = [
            "Self-Compassion: Acknowledge that you are doing the work of two people. Lower your expectations of perfection.",
            "Network Building: Identify one 'safe person' you can call when you feel your patience reaching its limit.",
            "Direct Line: Establish a 'Low-Energy Protocol' for days you are drained—focus on safety and connection over strict chores."
        ]
        yt_search = "single parent burnout and resilience psychology"
        return steps, "APA Parenting Resources | Mindfulness-Based Stress Reduction", yt_search

    # DEFAULT: General Psychology for Rules/Obedience
    elif any(word in query for word in ["obey", "rule", "listen"]):
        steps = [
            "Clarity: Ensure the rule is simple and stated positively (e.g., 'Please walk' vs 'Don't run').",
            "Consistency: Apply the same result every single time the rule is tested. Predictability creates safety.",
            "Direct Line: Use Logical Consequences. If the rule is broken, the privilege associated with that rule is paused."
        ]
        yt_search = "positive discipline authoritative parenting expert"
        return steps, "Positive Discipline Network | Yale ABCs of Child Rearing", yt_search

    return None, None, None

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #DDB892 !important; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #6B4423 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: 700 !important; }
    .wisdom-vault {
        background-color: #EDE0D4 !important; padding: 25px; border-radius: 15px;
        border-left: 12px solid #6B4423; display: flex; align-items: center; margin-bottom: 20px;
    }
    .stRadio { background-color: #6B4423 !important; padding: 15px; border-radius: 12px; }
    .stRadio label { color: #FFFFFF !important; font-weight: 700 !important; }
    .step-card { background: #EDE0D4; border-radius: 15px; padding: 20px; border: 2px solid #7F5539; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
partner_mode = st.sidebar.selectbox("Your Role:", ["Married/Partnered", "Single Parent", "Co-Parenting"])
partner_name = st.sidebar.text_input("Partner/Co-Parent Name", "Partner")
grace_state = st.sidebar.select_slider("Current Atmosphere:", options=["Peaceful", "Tense", "Conflict", "Crisis"])

# --- MAIN UI ---
st.title("Guardian Universal Partner")
quote, author = fetch_zen_wisdom()
st.markdown(f'<div class="wisdom-vault"><div style="font-size:50px; margin-right:25px;">🛡️</div><div><p style="font-size:1.2rem; font-weight:800; font-style:italic; margin:0;">{quote}</p><p style="font-weight:600; margin-top:5px;">{author}</p></div></div>', unsafe_allow_html=True)

if st.button("For Wisdom"):
    st.rerun()

st.divider()
user_input = st.text_input("What is on your heart? (Children, Partners, or Self-Growth)", placeholder="e.g., How do I handle a disagreement with my co-parent?")

if user_input:
    steps, res_text, yt_topic = get_universal_guidance(user_input, partner_mode)
    
    if steps:
        st.markdown(f"#### Guidance for: {user_input}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h5>Step 1: The Start</h5><p>{steps[0]}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h5>Step 2: The Action</h5><p>{steps[1]}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h5>The Direct Line</h5><p>{steps[2]}</p></div>', unsafe_allow_html=True)
        
        # SAFE SEARCH YOUTUBE
        yt_safe_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(yt_topic)}&sp=EgIoAQ%253D%253D"
        st.link_button("🎥 Watch Expert Guidance on this Topic", yt_safe_url)
        st.caption(f"Evidence-Based Resources: {res_text}")
    else:
        st.warning("I am here to help with child behavior, relationship health, or co-parenting peace. Try using keywords like 'rule', 'partner', or 'co-parent'.")

st.markdown("<br><h4 style='text-align: center;'>✨ Accountable. Gracious. Firm. ✨</h4>", unsafe_allow_html=True)

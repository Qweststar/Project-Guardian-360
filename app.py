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
    # Forces the page to refresh and pull a new quote/affirmation
    st_autorefresh(interval=10000, key="wisdom_refresh")

# --- REINFORCED WISDOM ENGINE (Fixed Error Handling) ---
def fetch_zen_wisdom():
    # Pre-defined fallbacks to prevent "NoneType" unpacking errors
    fallbacks = [
        ("“Integrity is doing the right thing, even when no one is watching.”", "— C.S. Lewis"),
        ("“Consistency is the highest form of love.”", "— Guardian Principle"),
        ("“I am the calm in my child's storm.”", "— Parent Affirmation"),
        ("“Firmness and Grace are the two wings of the Guardian.”", "— Mentorship Core")
    ]
    try:
        # Cache-buster forces a fresh pull from the ZenQuotes API
        url = f"https://zenquotes.io/api/random?cb={random.randint(1, 100000)}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                return str(data[0].get('q', fallbacks[0][0])), f"— {data[0].get('a', 'Unknown')}"
    except Exception:
        pass
    # Guaranteed to return a valid tuple if the API fails
    return random.choice(fallbacks)

# --- UNIVERSAL ADVISOR ENGINE ---
def get_universal_guidance(query):
    query = query.lower().strip()
    
    # CASE: Co-Parenting Accountability
    if any(word in query for word in ["co-parent", "ex-", "exchange", "custody"]):
        steps = [
            "Parallel Parenting: Keep communication strictly about logistics. Avoid emotional topics.",
            "The Business Model: Treat interactions like a professional meeting—polite and concise.",
            "Direct Line: If boundaries are crossed, revert to the written parenting plan immediately."
        ]
        yt_search = "high conflict co-parenting parallel parenting"
        return steps, "BIFF Method | Parallel Parenting Research", yt_search

    # CASE: Partnership / Marriage Strength
    elif any(word in query for word in ["partner", "marriage", "wife", "husband"]):
        steps = [
            "Soft Start-up: Bring up concerns without blame using 'I feel' statements.",
            "Accountability: Acknowledge your triggers and take responsibility for your part in the conflict.",
            "Direct Line: When tensions rise, use a 20-minute 'Positive Timeout' to calm down."
        ]
        yt_search = "Gottman method marriage accountability"
        return steps, "Gottman Institute Research", yt_search

    # CASE: Obedience / Rules
    elif any(word in query for word in ["obey", "rule", "listen", "discipline"]):
        steps = [
            "Clarity: State the rule positively and ensure the child understands the 'Why'.",
            "Consistency: Apply the result every time to create a predictable environment.",
            "Direct Line: Use Logical Consequences related to the broken rule."
        ]
        yt_search = "positive discipline authoritative parenting"
        return steps, "Positive Discipline Network", yt_search

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
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stRadio { background-color: #6B4423 !important; padding: 15px; border-radius: 12px; }
    .stRadio label { color: #FFFFFF !important; font-weight: 700 !important; }
    .step-card { background: #EDE0D4; border-radius: 15px; padding: 20px; border: 2px solid #7F5539; margin-bottom: 15px; }
    .stTextInput input { background-color: #F5EBE0 !important; color: #000000 !important; border: 2px solid #6B4423 !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & TOP WISDOM ---
partner_mode = st.sidebar.selectbox("Your Role:", ["Married/Partnered", "Single Parent", "Co-Parenting"])
partner_name = st.sidebar.text_input("Partner/Co-Parent Name", "Partner")
grace_state = st.sidebar.select_slider("Atmosphere:", options=["Peaceful", "Tense", "Conflict", "Crisis"])

st.title("Guardian Universal Partner")

# Error-proof Wisdom Fetch
quote_tuple = fetch_zen_wisdom()
quote, author = quote_tuple

st.markdown(f"""
    <div class="wisdom-vault">
        <div style="font-size:50px; margin-right:25px;">🛡️</div>
        <div>
            <p style="font-size:1.2rem; font-weight:800; font-style:italic; margin:0;">{quote}</p>
            <p style="font-weight:600; margin-top:5px;">{author}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.button("For Wisdom"):
    st.rerun()

st.divider()

# --- SEARCH & GUIDANCE ---
user_input = st.text_input("What is on your heart? (Children, Partners, or Growth)", placeholder="e.g., How do I stay calm during a disagreement?")

if user_input:
    steps, res_text, yt_topic = get_universal_guidance(user_input)
    
    if steps:
        st.markdown(f"#### Guidance for: *{user_input}*")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="step-card" style="border-left: 8px solid #B5838D;"><h5>Step 1</h5><p>{steps[0]}</p></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="step-card" style="border-left: 8px solid #E5989B;"><h5>Step 2</h5><p>{steps[1]}</p></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="step-card" style="border-left: 8px solid #6D597A;"><h5>The Direct Line</h5><p>{steps[2]}</p></div>', unsafe_allow_html=True)
        
        # SAFE SEARCH YOUTUBE (Restricted to educational content)
        yt_safe_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(yt_topic)}&sp=EgIoAQ%253D%253D"
        st.link_button("🎥 Explore Expert Guidance & Courses", yt_safe_url)
        st.caption(f"Psychological Frameworks: {res_text}")
    else:
        st.info("I am learning. Try keywords like 'partner', 'co-parent', or 'rules' to get specific guidance.")

st.markdown("<br><h4 style='text-align: center;'>✨ Firmness and Grace in every step. ✨</h4>", unsafe_allow_html=True)

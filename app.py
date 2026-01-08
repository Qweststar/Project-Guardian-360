import streamlit as st
import datetime

# --- PROJECT GUARDIAN 360: PROTOTYPE BUILD ---
# NOTE FOR FINAL PROTOTYPE:
# 1. Add Password Gate for family privacy.
# 2. Implement Fernet Encryption for the History Log.
# 3. Connect to a persistent database (Supabase/Firebase).

def get_tiered_responses(user_input, age_group):
    # Python is case-sensitive, so we normalize for better matching
    lookup = user_input.lower().strip()
    
    # 1. SAFETY GATE
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "⚠️ SAFETY ALERT: Please pause. If you are in crisis, call or text 988 immediately."

    # 2. THE GUARDIAN LIBRARY
    child_library = {
        "running": ["Walk inside, please.", "Walking feet only. If you run again, you'll sit for a reset.", "Since you can't walk safely, we're stopping this activity now."],
        "hit": ["Hands are for helping.", "No hitting. If it happens again, the play session ends.", "You chose to hit. Playtime is over while we calm down."],
        "lying": ["It feels like you might not be telling the whole story. Let's try again.", "I need the truth to help you. If you keep hiding it, we can't move forward.", "You chose to be dishonest. We are stopping this until we can repair the trust."],
        "disrespect": ["That tone isn't helpful. Let's try speaking respectfully.", "I'll listen when you use a calm voice. If you continue, I will walk away.", "I will not be spoken to that way. This conversation is over until you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Let's put the phones away for dinner.", "No phones at the table. Put it in the basket now.", "The phone is staying with me until tomorrow morning."],
        "room": ["Need help getting started on your room?", "The room needs to be clean by 6 PM to go out tonight.", "The room isn't clean. Plans are cancelled until the job is done."],
        "late": ["You're late. Let's be mindful of the time.", "Coming home late is a safety issue. We need to reset trust.", "You broke curfew. You are staying home next weekend to reset."],
        "lying": ["I'm giving you a chance to be honest right now.", "I already know the truth. Lying only makes it worse.", "Trust is broken. You will lose access to [privilege] for a week while we rebuild your word."],
        "disrespect": ["I hear you're frustrated, but that tone is unacceptable.", "We can disagree, but you will remain respectful.", "Respect is a requirement. Your [privilege] is suspended until we communicate properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    return [f"Gentle redirection for '{user_input}'.", f"Firm boundary for '{user_input}'.", f"The Direct Line: Consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

st.set_page_config(page_title="Guardian 360", layout="wide")

# Sidebar
st.sidebar.title("🛡️ Guardian 360")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("How is your child feeling?", options=["Calm", "Tired", "Stressed", "Meltdown"])

# Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

# Main Interface
st.title("Guardian Response Partner")
st.warning("🛠️ PROTOTYPE MODE: Data in the History Log is currently unencrypted. Do not enter sensitive names.")

age = st.radio("Who are we talking to?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What's happening? (Type and press Enter)", placeholder="e.g., They are running in the kitchen")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"**Step 1:**\n{responses[0]}")
        with col2:
            st.warning(f"**Step 2:**\n{responses[1]}")
        with col3:
            st.error(f"**The Direct Line:**\n{responses[2]}")
            
        if st.button("📝 Log This Incident"):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append({
                "Time": timestamp,
                "Behavior": user_input,
                "Context": grace_context
            })
            st.toast("Logged to history.")

# History Display
st.divider()
with st.expander("📊 View Behavioral History"):
    if st.session_state.history:
        st.table(st.session_state.history)
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No incidents logged yet.")

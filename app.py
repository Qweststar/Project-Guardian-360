import streamlit as st
import datetime

# --- ENHANCED UI FOR VISUAL CLARITY ---
st.markdown("""
    <style>
    /* Force a clean, high-contrast background */
    .stApp {
        background-color: #FDFBFA !important;
        color: #1A2F2F !important;
    }
    
    /* Sidebar Styling - Dark for distinct contrast */
    [data-testid="stSidebar"] {
        background-color: #1A2F2F !important;
        color: #FFFFFF !important;
    }
    
    /* Fixing Radio Button Visibility (Child/Teen) */
    .stRadio [data-testid="stWidgetLabel"] {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #006D77 !important;
        margin-bottom: 10px !important;
    }

    /* Step Card Styling - Neumorphic but high contrast */
    .step-card {
        background: #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #006D77;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Header colors */
    h1, h2, h3 {
        color: #006D77 !important;
    }
    
    /* Text Input Styling */
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 10px !important;
        color: #1A2F2F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---

def get_tiered_responses(user_input, age_group):
    lookup = user_input.lower().strip()
    
    # SAFETY GATE
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Let's Pause.** It sounds like things are very difficult right now. Your safety and your family's safety come first. Please reach out for support at 988 or local emergency services."

    # THE GUARDIAN LIBRARY (Human-to-Human Phrasing)
    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, let's take a quick reset break.", "Since it’s hard to stay safe right now, we’re going to pause this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, the play session ends.", "You chose to hit, so playtime is over. Let's find a way to calm down together."],
        "lying": ["It feels like there's more to the story. I'm ready to hear the truth.", "I can only help you when I know what really happened.", "Trust is the anchor. Because you chose to be dishonest, we are pausing until we repair that trust."],
        "disrespect": ["I can hear your frustration, but let's try a more respectful tone.", "I’m here to listen, but only when you use a calm voice.", "I value our relationship too much for this tone. We'll talk again when you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Could we put the phones away so we can enjoy dinner together?", "The rule is no phones at the table. Please put it in the basket now.", "I'll hold onto the phone until tomorrow morning to help you reset."],
        "room": ["I noticed the room needs some attention. Need a hand?", "The room needs to be clean by 6 PM to go out tonight.", "The room isn't ready. Plans for tonight are on hold until the job is done."],
        "late": ["I noticed you were a bit late. Let's check in on the time.", "Coming home past curfew is a safety concern. We need to reset our trust.", "You broke curfew. We'll stay home next weekend to rebuild that trust."],
        "lying": ["I'm giving you a safe space to be honest right now.", "I already know the truth. Lying just makes the situation heavier.", "Our trust is broken. Privilege is suspended while we rebuild your word."],
        "disrespect": ["I hear your frustration, but I need you to communicate that respectfully.", "We can disagree, but you must remain respectful.", "Respect is a requirement. [Privilege] is suspended until we can communicate properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    return [f"Try a gentle redirection regarding '{user_input}'.", f"State a clear, firm expectation for '{user_input}'.", f"Direct Line: It's time to enforce the consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

st.sidebar.title("🛡️ Project Guardian 360")
st.sidebar.markdown("*“Firmness and Grace in every step.”*")
partner_name = st.sidebar.text_input("Who is your partner in this?", "Partner")
grace_context = st.sidebar.select_slider("How is your child feeling?", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Response Partner")
st.markdown("### Take a breath. You've got this. 🌿")

if grace_context == "Meltdown":
    st.info("✨ **A Moment for Grace:** Your child's system is overwhelmed. Focus on Step 1.")
elif grace_context == "Stressed":
    st.info("✨ **A Moment for Grace:** Keep things low-key. Try Step 1 or 2.")

st.divider()

# High-Visibility Selection for Child/Teen
age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)

user_input = st.text_input("What's on your heart? (Type and press Enter)", placeholder="e.g., They are being disrespectful...")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        st.markdown("#### Here is your path forward:")
        
        # Displaying responses in high-contrast Step Cards
        st.markdown(f"""
        <div class="step-card" style="border-left-color: #2E7D32;">
            <h4 style='margin: 0; color: #2E7D32;'>Step 1: The Gentle Start</h4>
            <p style='color: #1A2F2F; font-size: 1.1rem;'>{responses[0]}</p>
        </div>
        <div class="step-card" style="border-left-color: #EF6C00;">
            <h4 style='margin: 0; color: #EF6C00;'>Step 2: The Firm Expectation</h4>
            <p style='color: #1A2F2F; font-size: 1.1rem;'>{responses[1]}</p>
        </div>
        <div class="step-card" style="border-left-color: #C62828;">
            <h4 style='margin: 0; color: #C62828;'>Step 3: The Direct Line</h4>
            <p style='color: #1A2F2F; font-size: 1.1rem;'>{responses[2]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Record this moment for later"):
            st.toast("Saved to your patterns of growth. 🌿")

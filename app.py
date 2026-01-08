import streamlit as st
import datetime

# --- FORCED DARK MODE & SKY BLUE PALETTE ---
st.markdown("""
    <style>
    /* Force Dark Mode Background */
    .stApp {
        background-color: #0F172A !important; /* Deep Night Blue/Stone */
        color: #E2E8F0 !important; /* Soft White Text */
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
    
    /* SKY BLUE HEADERS */
    h1, h2, h3, h4 {
        color: #7DD3FC !important; /* Sky Blue */
        font-family: 'Inter', sans-serif;
    }

    /* FIXING THE RADIO BUTTONS (Child/Teen) */
    /* We wrap them in a high-contrast container for visibility */
    .stRadio {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #38B2AC;
    }
    
    .stRadio [data-testid="stWidgetLabel"] {
        color: #7DD3FC !important;
        font-weight: 700 !important;
    }

    /* STEP CARDS - High Contrast for Dark Mode */
    .step-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* Input Box Visibility */
    .stTextInput input {
        background-color: #0F172A !important;
        color: #7DD3FC !important;
        border: 1px solid #334155 !important;
    }
    
    /* Success/Warning/Error Overrides for the Sky palette */
    .stAlert {
        background-color: #1E293B !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---

def get_tiered_responses(user_input, age_group):
    # Case sensitivity check: Python is case-sensitive, so we use .lower()
    lookup = user_input.lower().strip()
    
    # SAFETY GATE
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Let's Pause.** Safety comes first. Please reach out for support at 988 or local emergency services."

    # THE GUARDIAN LIBRARY
    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, we'll take a reset break.", "Since safety is hard right now, we’re going to pause this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, the play session ends.", "You chose to hit, so playtime is over. Let's calm down together."],
        "lying": ["It feels like there's more to the story. I'm ready for the truth.", "I can only help you when I know the real story.", "Trust is our anchor. Because of the dishonesty, we're pausing until we repair it."],
        "disrespect": ["Let's try a more respectful tone, please.", "I'll listen when you use a calm voice. If this continues, I'll step away.", "I value us too much for this tone. We'll talk when you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Could we put the phones away so we can enjoy dinner?", "The rule is no phones at the table. Please put it in the basket now.", "I'll hold onto the phone until morning to help you reset."],
        "room": ["Need a hand getting started on your room?", "The room needs to be clean by 6 PM to go out. How's it coming?", "The room isn't ready. Plans for tonight are on hold until it's done."],
        "late": ["I noticed you were a bit late. Let's be mindful next time.", "Being late is a safety concern. We need to reset our trust.", "You broke curfew. We'll stay home next weekend to rebuild that trust."],
        "lying": ["I'm giving you a safe space to be honest right now.", "I already know the truth. Lying just makes the situation heavier.", "Trust is broken. Privilege is suspended while we rebuild your word."],
        "disrespect": ["I hear your frustration, but please communicate that respectfully.", "We can disagree, but you must remain respectful.", "Respect is required. [Privilege] is suspended until we communicate properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    return [f"Gentle redirection for '{user_input}'.", f"Firm expectation for '{user_input}'.", f"Direct Line: Enforce consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

st.sidebar.title("🛡️ Project Guardian 360")
st.sidebar.markdown("*Firmness and Grace.*")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("Child's State", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Partner")
st.markdown("#### Take a breath. Everything is going to be okay. 🌿")

# Grace Consultant
if grace_context == "Meltdown":
    st.info("✨ **Grace Note:** Focus only on Step 1 right now.")
elif grace_context == "Stressed":
    st.info("✨ **Grace Note:** Keep things low-key. Step 1 or 2 is best.")

st.divider()

# High-Visibility Selection
age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)

user_input = st.text_input("What's on your heart? (Type and Enter)", placeholder="Type here...")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        st.markdown("### The Path Forward")
        
        # Displaying responses in High-Contrast Sky Blue Cards
        st.markdown(f"""
        <div class="step-card" style="border-top: 4px solid #38B2AC;">
            <h4 style='margin: 0;'>Step 1: The Gentle Start</h4>
            <p style='color: #BAE6FD; font-size: 1.1rem;'>{responses[0]}</p>
        </div>
        <div class="step-card" style="border-top: 4px solid #F6AD55;">
            <h4 style='margin: 0;'>Step 2: The Firm Expectation</h4>
            <p style='color: #FFEDD5; font-size: 1.1rem;'>{responses[1]}</p>
        </div>
        <div class="step-card" style="border-top: 4px solid #F56565;">
            <h4 style='margin: 0;'>Step 3: The Direct Line</h4>
            <p style='color: #FEE2E2; font-size: 1.1rem;'>{responses[2]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Record Progress"):
            st.toast("Saved to your patterns of growth. 🌿")

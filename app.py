import streamlit as st
import datetime

# --- FORCED WARM EARTH & OLIVE ACCENT THEME ---
st.markdown("""
    <style>
    /* 70% of the page: Warm Beige / Sand Background */
    .stApp {
        background-color: #F2E9E4 !important; /* Soft Sand/Beige */
        color: #222222 !important; /* High contrast Dark Charcoal text */
    }
    
    /* Sidebar Styling - Deep Olive for Anchor */
    [data-testid="stSidebar"] {
        background-color: #354F52 !important; /* Deep Forest/Olive */
        color: #F8FAF8 !important;
    }
    
    /* OLIVE ACCENT HEADERS */
    h1, h2, h3, h4 {
        color: #52796F !important; /* Muted Olive Green */
        font-family: 'Inter', sans-serif;
    }

    /* SELECTION CONTAINER (Child/Teen) - Olive Accent */
    .stRadio {
        background-color: #CAD2C5; /* Light Sage/Beige Mix */
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #84A98C; /* Olive border */
    }
    
    .stRadio [data-testid="stWidgetLabel"] {
        color: #2F3E46 !important;
        font-weight: 700 !important;
    }

    /* STEP CARDS - Soft Beige with Olive Borders */
    .step-card {
        background: #FFFFFF; /* Pure white for readability */
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #D1C7C1;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Input Box Visibility */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #222222 !important;
        border: 2px solid #CAD2C5 !important;
    }
    
    /* Alert Overrides */
    .stAlert {
        background-color: #CAD2C5 !important;
        color: #2F3E46 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---

def get_tiered_responses(user_input, age_group):
    # Python is case-sensitive: normalizing to lowercase for better matching
    lookup = user_input.lower().strip()
    
    # SAFETY GATE
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Safety First.** If things feel out of control, please pause and reach out for help at 988. We are here to support a safe environment."

    # THE GUARDIAN LIBRARY
    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, let's take a reset break.", "Since safety is hard right now, we’re going to pause this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, the play session ends.", "You chose to hit, so playtime is over. Let's find a way to calm down together."],
        "lying": ["It feels like there's more to the story. I'm ready for the truth.", "I can only help you when I know what really happened.", "Trust is the anchor. Because of the dishonesty, we're pausing until we repair it."],
        "disrespect": ["I hear your frustration, but let's try a more respectful tone.", "I'm here to listen, but only when you use a calm voice.", "I value our relationship too much for this tone. We'll talk again when you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Could we put the phones away so we can enjoy dinner together?", "The rule is no phones at the table. Please put it in the basket now.", "I'll hold onto the phone until tomorrow morning to help you reset."],
        "room": ["I noticed the room needs some attention. Need a hand getting started?", "The room needs to be clean by 6 PM to go out. How's it coming?", "The room isn't ready. Plans for tonight are on hold until the job is done."],
        "late": ["I noticed you were a bit late. Let's be mindful of the time next time.", "Coming home past curfew is a safety concern. We need to reset our trust.", "You broke curfew. We'll stay home next weekend to rebuild that trust."],
        "lying": ["I'm giving you a safe space to be honest right now.", "I already know the truth. Lying just makes the situation heavier.", "Our trust is broken. Privilege is suspended while we rebuild your word."],
        "disrespect": ["I hear your frustration, but please communicate that respectfully.", "We can disagree, but you must remain respectful.", "Respect is a requirement. [Privilege] is suspended until we communicate properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    return [f"Try a gentle redirection regarding '{user_input}'.", f"State a clear, firm expectation for '{user_input}'.", f"Direct Line: Enforce the consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

st.sidebar.title("🛡️ Project Guardian 360")
st.sidebar.markdown("*Firmness and Grace.*")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("Child's State", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Partner")
st.markdown("#### Take a breath. Everything is going to be okay. 🌿")

# Grace Consultant
if grace_context == "Meltdown":
    st.info("✨ **Grace Note:** Focus only on Step 1 right now. Prioritize connection.")
elif grace_context == "Stressed":
    st.info("✨ **Grace Note:** Keep things low-key. Step 1 or 2 is likely enough.")

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
        
        # Displaying responses in High-Contrast Earth/Olive Cards
        st.markdown(f"""
        <div class="step-card" style="border-left: 6px solid #84A98C;">
            <h4 style='margin: 0; color: #52796F;'>Step 1: The Gentle Start</h4>
            <p style='color: #222222; font-size: 1.1rem;'>{responses[0]}</p>
        </div>
        <div class="step-card" style="border-left: 6px solid #E9C46A;">
            <h4 style='margin: 0; color: #B08E35;'>Step 2: The Firm Expectation</h4>
            <p style='color: #222222; font-size: 1.1rem;'>{responses[1]}</p>
        </div>
        <div class="step-card" style="border-left: 6px solid #E76F51;">
            <h4 style='margin: 0; color: #AF4D36;'>Step 3: The Direct Line</h4>
            <p style='color: #222222; font-size: 1.1rem;'>{responses[2]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Record Progress"):
            st.toast("Saved to your family patterns. 🌿")

import streamlit as st
import datetime

# --- FORCED AUTUMN EARTH & PURE BLACK TEXT THEME ---
st.markdown("""
    <style>
    /* Main Background: Light Autumn Brown / Tan */
    .stApp {
        background-color: #DDB892 !important; /* Autumn Tan */
        color: #000000 !important; /* PURE BLACK TEXT */
    }
    
    /* Sidebar: Deep Olive Forest */
    [data-testid="stSidebar"] {
        background-color: #344E41 !important; 
        color: #000000 !important;
    }

    /* Force all sidebar text to Black for visibility */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Headers in Deep Olive - Forced to Black for your request */
    h1, h2, h3, h4 {
        color: #000000 !important; 
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
    }

    /* Selection Container (Child/Teen) - Olive Background with Black Text */
    .stRadio {
        background-color: #A3B18A; /* Muted Olive */
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #344E41;
    }
    
    .stRadio label {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* STEP CARDS - Slightly lighter Tan/Beige for contrast */
    .step-card {
        background: #EDE0D4; /* Soft Beige Card */
        border-radius: 12px;
        padding: 20px;
        border: 2px solid #7F5539; /* Brown border */
        margin-bottom: 20px;
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* PURE BLACK TEXT FOR CARDS */
    .step-card p, .step-card h4 {
        color: #000000 !important;
    }
    
    /* Input Box Visibility */
    .stTextInput input {
        background-color: #EDE0D4 !important;
        color: #000000 !important;
        border: 2px solid #7F5539 !important;
        font-weight: 600 !important;
    }
    
    /* Alerts - Soft Autumn Sage */
    .stAlert {
        background-color: #A3B18A !important;
        color: #000000 !important;
        border: 1px solid #344E41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---

def get_tiered_responses(user_input, age_group):
    # Python is case-sensitive, so we normalize for reliable library matching
    lookup = user_input.lower().strip()
    
    # SAFETY GATE
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Safety Alert.** Please pause. If things feel unsafe, call 988. We prioritize a safe home above all else."

    # THE GUARDIAN LIBRARY
    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Walking feet only. If you run again, we'll take a reset break.", "Since safety is hard right now, we’re going to pause this activity."],
        "hit": ["Let's use our helping hands.", "No hitting. If it happens again, the play session ends.", "You chose to hit, so playtime is over. Let's calm down together."],
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
            
    return [f"Step 1: Gentle redirection for '{user_input}'.", f"Step 2: Firm expectation for '{user_input}'.", f"Step 3: Direct Line consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

st.sidebar.title("🛡️ Guardian 360")
st.sidebar.markdown("*Firmness and Grace.*")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("How is your child feeling?", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Response Partner")
st.markdown("### Take a breath. You've got this. 🌿")

# Grace Consultant
if grace_context == "Meltdown":
    st.info("✨ **Grace Note:** The child is overwhelmed. Focus on Step 1 only.")
elif grace_context == "Stressed":
    st.info("✨ **Grace Note:** Patience is key. Try Step 1 or 2 first.")

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
        
        # Displaying responses in High-Contrast Autumn Cards
        st.markdown(f"""
        <div class="step-card" style="border-left: 8px solid #344E41;">
            <h4 style='margin: 0;'>Step 1: The Gentle Start</h4>
            <p style='font-size: 1.15rem;'>{responses[0]}</p>
        </div>
        <div class="step-card" style="border-left: 8px solid #BC6C25;">
            <h4 style='margin: 0;'>Step 2: The Firm Expectation</h4>
            <p style='font-size: 1.15rem;'>{responses[1]}</p>
        </div>
        <div class="step-card" style="border-left: 8px solid #606C38;">
            <h4 style='margin: 0;'>Step 3: The Direct Line</h4>
            <p style='font-size: 1.15rem;'>{responses[2]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Record Progress"):
            st.toast("Saved to your family history. 🌿")

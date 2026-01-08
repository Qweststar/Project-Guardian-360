import streamlit as st
import datetime

# --- CUSTOM CSS FOR THE "HUMAN" LOOK & FEEL ---
# Implementing soft UI, calming colors, and clean typography
st.markdown("""
    <style>
    /* Background and global font */
    .stApp {
        background-color: #fcf8f6; /* Ivory / Soft Off-White */
        color: #2c3e50;
    }
    /* Soft 'Neumorphic' cards for steps */
    .step-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 8px 8px 16px #e0e0e0, -8px -8px 16px #ffffff;
        margin-bottom: 20px;
        border: none;
    }
    /* Custom headers */
    h1, h2, h3 {
        color: #006d77; /* Deep Teal - Trustworthy & Calm */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Styling the radio buttons and text areas to be softer */
    .stRadio > div {
        flex-direction: row;
        gap: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC (Sequential Guidance) ---

def get_tiered_responses(user_input, age_group):
    lookup = user_input.lower().strip()
    
    # 1. THE SAFETY NET
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "✋ **Let's Pause.** It sounds like things are very difficult right now. Your safety and your family's safety come first. Please reach out for support at 988 or local emergency services."

    # 2. THE GUARDIAN LIBRARY (Human-to-Human Phrasing)
    child_library = {
        "running": ["I'd love to see you walk inside, please.", "Remember, we use walking feet to keep everyone safe. If you run again, let's take a quick reset break.", "Since it’s hard to stay safe right now, we’re going to pause this activity and try again later."],
        "hit": ["Let's use our helping hands.", "We don't hit in this family. If it happens again, we'll have to stop playing for now.", "You chose to hit, so playtime is over. Let's find a way to calm down together."],
        "lying": ["It feels like there's more to the story. I'm ready to hear the truth.", "I can only help you when I know what really happened. If we can't be honest, we can't move forward with this.", "Trust is the anchor of our family. Because you chose to be dishonest, we are going to pause everything until we can repair that trust."],
        "disrespect": ["I can hear your frustration, but let's try a more respectful tone.", "I’m here to listen, but only when you use a calm voice. If the disrespect continues, I’ll need to step away for a moment.", "I value our relationship too much to let us speak to each other this way. We'll talk again when you can lead with respect."]
    }
    
    teen_library = {
        "phone": ["Could we put the phones away so we can enjoy dinner together?", "The rule is no phones at the table. Please put it in the basket now so we can focus on each other.", "You're choosing the phone over our family boundary. I'll hold onto it until tomorrow morning to help you reset."],
        "room": ["I noticed the room needs some attention. Do you need a hand getting started?", "I'd love for you to go out tonight, but the room needs to be clean by 6 PM first. How's it coming along?", "The room isn't ready as we agreed. Plans for tonight are on hold until the job is done."],
        "late": ["I noticed you were a bit late. Let's check in on the time next time.", "Coming home past curfew is a safety concern for me. We need to reset our trust. How can we make this better?", "You broke our curfew agreement. We'll stay home next weekend to focus on rebuilding that trust and safety."],
        "lying": ["I'm giving you a safe space to be honest with me right now.", "I already know the truth, and I'd much rather hear it from you. Lying just makes the situation heavier.", "Our trust is broken. You'll lose access to your [privilege] for a week while we work together on rebuilding your word."],
        "disrespect": ["I hear your frustration, but I need you to communicate that respectfully.", "We can disagree, but you must remain respectful. If you can't, let's take a break from this conversation.", "Respect is a requirement in this home. Because of the choice you made, [privilege] is suspended until we can talk properly."]
    }

    library = teen_library if age_group == "Teen" else child_library
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    return [f"Try a gentle redirection regarding '{user_input}'.", f"State a clear, firm expectation for '{user_input}'.", f"Direct Line: It's time to enforce the consequence for '{user_input}'."], None

# --- UI CONFIGURATION ---

# Sidebar for a warm welcome
st.sidebar.title("🛡️ Project Guardian 360")
st.sidebar.markdown("*“Firmness and Grace in every step.”*")
partner_name = st.sidebar.text_input("Who is your partner in this?", "Partner")
grace_context = st.sidebar.select_slider("How is your child feeling right now?", options=["Calm", "Tired", "Stressed", "Meltdown"])

# Main Header
st.title("Guardian Response Partner")
st.markdown("### Take a breath. You've got this. 🌿")

# Grace Consultant (Now feels like a supportive nudge)
if grace_context == "Meltdown":
    st.info("✨ **A Moment for Grace:** Your child's system is overwhelmed. Focus on Step 1. Connection is more important than the rule right now.")
elif grace_context == "Stressed":
    st.info("✨ **A Moment for Grace:** Everyone is a little tired. Keep things low-key and try to stay at Step 1 or 2 if possible.")

# Input Section
st.divider()
age = st.radio("Who are we talking with?", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What's on your heart? (Type and press Enter)", placeholder="e.g., They are being disrespectful...")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        st.markdown("#### Here is your path forward:")
        
        # Displaying responses in 'Human' cards
        st.markdown(f"""
        <div class="step-card">
            <h4 style='margin-top:0;'>Step 1: The Gentle Start</h4>
            <p style='color: #2e7d32;'>{responses[0]}</p>
        </div>
        <div class="step-card">
            <h4 style='margin-top:0;'>Step 2: The Firm Expectation</h4>
            <p style='color: #ef6c00;'>{responses[1]}</p>
        </div>
        <div class="step-card">
            <h4 style='margin-top:0;'>Step 3: The Direct Line</h4>
            <p style='color: #c62828;'>{responses[2]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Record this moment for later"):
            # Simple session history
            if "history" not in st.session_state: st.session_state.history = []
            timestamp = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.history.append({"Time": timestamp, "Incident": user_input, "State": grace_context})
            st.toast("Saved to your family log. 🌿")

# History Section
with st.expander("📊 Review Our Progress Together"):
    if "history" in st.session_state and st.session_state.history:
        st.write("### Patterns of Growth")
        st.table(st.session_state.history)
    else:
        st.write("No incidents recorded. You're doing a great job maintaining a peaceful home.")

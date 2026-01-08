import streamlit as st

# --- PROJECT GUARDIAN 360: STREAMLINED TIERED BRAIN ---

def get_tiered_responses(user_input, age_group):
    lookup = user_input.lower().strip()
    
    # 1. SAFETY GATE (Non-negotiable)
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "⚠️ SAFETY ALERT: Stop. If you are in crisis, call or text 988 immediately. Safety is the only priority right now."

    # 2. THE GUARDIAN LIBRARY (Level 1, 2, 3)
    child_tiers = {
        "running": ["Walk inside, please.", "Walking feet only. If you run again, you'll sit for a reset.", "You can't walk safely, so we are stopping this activity now."],
        "hit": ["Hands are for helping.", "No hitting. If it happens again, the play session ends.", "You chose to hit. Playtime is over while we calm down."],
        "quiet": ["Indoor voice, please.", "It's too loud. Lower your volume or we take a 5-minute quiet break.", "The noise is too much. We are doing 5 minutes of quiet time now."],
        "dessert": ["Dinner first, then dessert.", "The rule is food before sugar. Finish your plate.", "You didn't eat dinner, so there is no dessert tonight."]
    }
    
    teen_tiers = {
        "phone": ["Let's put the phones away for dinner.", "No phones at the table. Put it in the basket now.", "The phone is staying with me until tomorrow morning."],
        "room": ["Need help getting started on your room?", "The room needs to be clean by 6 PM to go out tonight.", "The room isn't clean. Plans are cancelled until the job is done."],
        "late": ["You're late. Let's be mindful of the time.", "Coming home late is a safety issue. We need to reset trust.", "You broke curfew. You are staying home next weekend to reset."]
    }

    library = teen_tiers if age_group == "Teen" else child_tiers

    # Search for a match
    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    # AI-Style Fallback if no match
    return [
        f"L1 (Grace): Redirection for '{user_input}'.",
        f"L2 (Firm): Clear boundary for '{user_input}'.",
        f"L3 (Hard Truth): Consequence for '{user_input}'."
    ], None

# --- UI CONFIGURATION ---

st.set_page_config(page_title="Guardian 360", layout="wide")

st.sidebar.title("🛡️ Guardian 360")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("Grace Filter (Child's State)", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Response Engine")

# Integration of Grace Filter as an Assistant
if grace_context == "Meltdown":
    st.info("💡 **Grace Consultant:** Level 1 is highly recommended. The child is currently unable to process Level 3.")
elif grace_context == "Stressed":
    st.info("💡 **Grace Consultant:** Level 1 or 2 is best. Be firm but keep your tone low.")

# Main Input
age = st.radio("Age Group", ["Child", "Teen"], horizontal=True)
user_input = st.text_input("What are you about to say?", placeholder="Type and press Enter...")

if user_input:
    responses, safety_error = get_tiered_responses(user_input, age)
    
    if safety_error:
        st.error(safety_error)
    else:
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Level 1\n*Grace & Redirection*")
            st.success(responses[0])
        
        with col2:
            st.markdown("### Level 2\n*Firm Boundary*")
            st.warning(responses[1])
            
        with col3:
            st.markdown("### Level 3\n*Hard Truth/Consequence*")
            st.error(responses[2])

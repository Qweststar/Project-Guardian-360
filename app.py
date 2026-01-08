import streamlit as st

# --- PROJECT GUARDIAN 360: HUMAN-CENTERED RESPONSE ENGINE ---

def get_tiered_responses(user_input, age_group):
    lookup = user_input.lower().strip()
    
    # 1. SAFETY GATE (Python is case-sensitive, so we use .lower())
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return None, "⚠️ SAFETY ALERT: Stop. If you are in crisis, call or text 988 immediately. Safety is the priority right now."

    # 2. THE GUARDIAN LIBRARY (Taught Phrases)
    child_tiers = {
        "running": ["Walk inside, please.", "Walking feet only. If you run again, you'll sit for a reset.", "Since you can't walk safely, we're stopping this activity now."],
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

    for trigger, responses in library.items():
        if trigger in lookup:
            return responses, None
            
    # Default message if no exact match is found in the library
    return [
        f"Try a gentle redirection regarding '{user_input}'.",
        f"State a clear, firm boundary for '{user_input}'.",
        f"Take a Direct Line: Enforce the consequence for '{user_input}'."
    ], None

# --- UI CONFIGURATION ---

st.set_page_config(page_title="Guardian 360", layout="wide")

st.sidebar.title("🛡️ Guardian 360")
partner_name = st.sidebar.text_input("Partner Name", "Partner")
grace_context = st.sidebar.select_slider("How is your child feeling?", options=["Calm", "Tired", "Stressed", "Meltdown"])

st.title("Guardian Response Partner")

# Contextual Guidance based on the Grace Filter
if grace_context == "Meltdown":
    st.info("💡 **A Note on Grace:** Your child is overwhelmed. Focus on Step 1. They likely cannot process the 'Direct Line' consequence right now.")
elif grace_context == "Stressed":
    st.info("💡 **A Note on Grace:** Keep things low-key. Try Step 1 first, and only move forward if safety or respect is an issue.")

# Main Input Section
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
            st.markdown("### Step 1\n**Try this first:**")
            st.success(responses[0])
        
        with col2:
            st.markdown("### Step 2\n**If that didn't work:**")
            st.warning(responses[1])
            
        with col3:
            st.markdown("### Step 3\n**The Direct Line:**")
            st.error(responses[2])
            
        st.caption(f"Consistency is care. You and {partner_name} are working together.")

import streamlit as st

# --- PROJECT GUARDIAN 360: HYBRID BRAIN & GUARDRAILS ---

def guardian_hybrid_brain(user_input, age_group, partner_name, grace_level):
    """
    Combines your specific taught library with an AI fallback.
    Includes safety guardrails as the first priority.
    """
    # Python is case-sensitive; we normalize to lowercase for matching
    lookup = user_input.lower().strip()

    # 1. MANDATORY SAFETY GUARDRAILS
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return "⚠️ SAFETY ALERT: Please pause. We prioritize safety above all else. If you are in crisis, call or text 988 immediately. You are not alone."

    # 2. YOUR TAUGHT LIBRARY
    child_library = {
        "running": "Remember we walk when indoors.",
        "hit": "Hitting is not allowed. Hands are for helping.",
        "quiet": "Use your indoor voice please?",
        "crying": "I can see you are having a hard time. I'm here to help you.",
        "touch": "Let's keep our hands to ourselves for now.",
        "dessert": "We can have dessert after we finish dinner."
    }
    
    teen_library = {
        "phone": "Let's put the phones away for dinner?",
        "room": "We need to get this room clean. Do you need some help?",
        "talk back": f"Let us talk in a manner that is respectful. Keep in mind that I am still your {st.session_state.get('parent_role', 'Parent')}.",
        "late": "Coming home past curfew is unacceptable per your safety. How can we make sure it doesn't happen next time?"
    }

    library = teen_library if age_group == "Teen" else child_library

    # Check for manual matches first
    for trigger, response in library.items():
        if trigger in lookup:
            return f"🏠 (Library Match): {response}"

    # 3. AI BRAIN FALLBACK
    return (f"🧠 (AI Brain): I hear that you're dealing with '{user_input}'. "
            f"Given the {grace_level} stress level, I suggest focusing on a calm boundary "
            f"that shows respect for both yourself and {partner_name}.")

# --- STREAMLIT DASHBOARD CONFIG ---

st.set_page_config(page_title="Project Guardian 360", page_icon="🛡️")

# Sidebar for Personalization
st.sidebar.title("🛡️ Project Guardian 360")
parent_role = st.sidebar.text_input("Your Role (e.g. Mom/Dad)", "Parent", key="parent_role")
partner_name = st.sidebar.text_input("Partner Name", "Partner")

st.sidebar.divider()
st.sidebar.header("The Grace Filter")
grace_level = st.sidebar.select_slider(
    "Child's Emotional State",
    options=["Calm", "Tired", "Stressed", "Meltdown"]
)

# --- MAIN INTERFACE ---

st.title("Guardian Dashboard")
st.caption(f"Status: Unified Front with {partner_name}")

if grace_level == "Meltdown":
    st.error("🚨 **GRACE ALERT:** The child is overwhelmed. Prioritize safety and calm breathing first.")

tabs = st.tabs(["Direct Response", "Accountability", "Unified Front", "Hard Truths"])

with tabs[0]:
    st.header("Quick Rephrase")
    age = st.radio("Select Age Group", ["Child", "Teen"], horizontal=True)
    
    # Typing in this box and hitting ENTER will now trigger the response automatically
    user_input = st.text_input("What are you about to say?", placeholder="Type here and press Enter...")
    
    if user_input:
        # This code runs automatically as soon as the user presses Enter
        result = guardian_hybrid_brain(user_input, age, partner_name, grace_level)
        st.divider()
        st.subheader("The Recommended Path:")
        st.success(result)
        st.info("💡 Tip: You can type a new phrase above and hit Enter again to refresh.")

with tabs[1]:
    st.header("Parental Accountability")
    if st.button("I overreacted/yelled"):
        st.write(f"**The Repair Script:** 'I'm sorry I lost my cool. I shouldn't have taken my frustration out on you. Can we try again?'")

with tabs[2]:
    st.header("The Unified Front")
    option = st.selectbox("Situation", ["Support a partner's 'No'", "Modeling respect during a disagreement"])
    if option == "Support a partner's 'No'":
        st.warning(f"**The Unified Script:** '{partner_name} already gave you an answer, and I support that decision.'")
    else:
        st.info(f"**The Grace Script:** 'I see things differently than {partner_name}, but we will discuss it together later.'")

with tabs[3]:
    st.header("Hard Truths Knowledge Base")
    st.markdown("""
    - **No Sugar-Coating:** Be direct and clear.
    - **Accountability:** Own your mistakes to model health for your child.
    - **Grace:** Life isn't binary; allow room for human error.
    """)

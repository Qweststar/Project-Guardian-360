import streamlit as st

# --- PROJECT GUARDIAN 360: HYBRID BRAIN & GUARDRAILS ---

def guardian_hybrid_brain(user_input, age_group, partner_name, grace_level):
    """
    Combines your specific taught library with an AI fallback.
    Includes safety guardrails as the first priority.
    """
    # Python is case-sensitive, so we normalize for the lookup
    lookup = user_input.lower().strip()

    # 1. MANDATORY SAFETY GUARDRAILS
    # These override everything to prevent harm.
    danger_zone = ["hurt", "kill", "suicide", "hit", "abuse", "beat", "punch"]
    if any(word in lookup for word in danger_zone):
        return "⚠️ SAFETY ALERT: It sounds like things are reaching a breaking point. We prioritize safety above all else. Please pause and call or text 988 (Crisis Line) immediately to speak with a professional. You are not alone."

    # 2. YOUR TAUGHT LIBRARY (The Preferred Examples)
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

    # Select library based on age
    library = teen_library if age_group == "Teen" else child_library

    # Check for manual matches first
    for trigger, response in library.items():
        if trigger in lookup:
            return f"🏠 (Library Match): {response}"

    # 3. AI BRAIN FALLBACK (Non-Binary Logic: Firmness + Grace)
    # This prepares the prompt for the AI to follow your philosophy.
    return (f"🧠 (AI Brain Placeholder): I hear that you're dealing with '{user_input}'. "
            f"Given the {grace_level} stress level, I suggest focusing on a calm boundary "
            f"that shows respect for both yourself and {partner_name}.")

# --- STREAMLIT DASHBOARD CONFIG ---

st.set_page_config(page_title="Project Guardian 360", page_icon="🛡️")

# Sidebar for Personalization and the 'Grace Filter'
st.sidebar.title("🛡️ Project Guardian 360")
parent_role = st.sidebar.text_input("Your Role (e.g. Mom/Dad)", "Parent", key="parent_role")
partner_name = st.sidebar.text_input("Partner/Co-Parent Name", "Partner")

st.sidebar.divider()
st.sidebar.header("The Grace Filter")
grace_level = st.sidebar.select_slider(
    "Child's Emotional State",
    options=["Calm", "Tired", "Stressed", "Meltdown"]
)

# Emergency Sidebar Support
st.sidebar.divider()
if st.sidebar.button("🆘 EMERGENCY RESET"):
    st.sidebar.error("Take 5 deep breaths. Walk away if you need to. Your child needs a regulated adult more than they need a perfect response.")

# --- MAIN INTERFACE ---

st.title("Guardian Dashboard")
st.caption(f"Status: Unified Front with {partner_name} | Role: {parent_role}")

if grace_level == "Meltdown":
    st.error("🚨 **GRACE ALERT:** The child's nervous system is overwhelmed. Discipline will not work right now. Focus on safety, calm presence, and physical comfort first.")

tabs = st.tabs(["Direct Response", "Accountability", "Unified Front", "Hard Truths"])

with tabs[0]:
    st.header("Quick Rephrase")
    st.write("What are you about to say?") # Label for clarity
    age = st.radio("Select Age Group", ["Child", "Teen"], horizontal=True)
    
    # This is the "What are you about to say" portion
    user_input = st.text_input("Enter your phrase here:", placeholder="e.g., Stop running!")
    
    if st.button("Generate Guardian Response"):
        if user_input:
            # This triggers the function and shows the result
            result = guardian_hybrid_brain(user_input, age, partner_name, grace_level)
            st.subheader("The Recommended Path:")
            st.success(result)
        else:
            st.warning("Please type something in the box above so I can help you rephrase it.")

with tabs[1]:
    st.header("Parental Accountability")
    st.info("Being a well-adjusted adult means owning your mistakes. Use these to repair the relationship.")
    if st.button("I overreacted/yelled"):
        st.write(f"**The Repair Script:** 'I'm sorry I lost my cool. I was feeling frustrated, but I shouldn't have taken it out on you. Can we try that conversation again?'")

with tabs[2]:
    st.header("The Unified Front")
    st.write(f"Modeling respect for {partner_name} teaches your child how to treat others.")
    option = st.selectbox("Situation", ["Support a partner's 'No'", "Modeling respect during a disagreement"])
    
    if option == "Support a partner's 'No'":
        st.warning(f"**The Unified Script:** '{partner_name} already gave you an answer, and I support that decision. We are on the same team.'")
    else:
        st.info(f"**The Grace Script:** 'I see things differently than {partner_name}, but we will discuss it together and let you know our decision. We respect each other's opinions.'")

with tabs[3]:
    st.header("Hard Truths Knowledge Base")
    st.markdown("""
    ### ⚓ Guardian Core Values
    - **No Sugar-Coating:** Be direct. Children feel safer when the boundaries are clear and predictable.
    - **Modeling:** You are the blueprint. If you want them to be respectful, you must show respect to others—especially your co-parent.
    - **Accountability:** When you mess up, own it. It shows them that mistakes aren't the end of the world; they are for learning.
    - **Non-Binary Grace:** Life isn't black and white. A child can be wrong, but they still deserve to be treated with dignity.
    """)

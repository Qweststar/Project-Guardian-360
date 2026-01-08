import streamlit as st

# --- PROJECT GUARDIAN 360: CORE LOGIC ---

def get_rephrase(phrase, age_group):
    phrase = phrase.lower().strip()
    
    # Child Library
    if age_group == "Child":
        library = {
            "running": "Remember we walk when indoors.",
            "hit": "Hitting is not allowed. Hands are for helping.",
            "quiet": "Use your indoor voice please?",
            "crying": "I can see you are having a hard time. I'm here to help you.",
            "touch": "Let's keep our hands to ourselves for now.",
            "dessert": "We can have dessert after we finish dinner."
        }
    # Teenager Library (No sugar-coating, focus on respect)
    else: 
        library = {
            "phone": "Let's put the phones away for dinner?",
            "room": "We need to get this room clean. Do you need some help?",
            "talk back": "Let us talk in a manner that is respectful. Keep in mind that I am still your parent.",
            "late": "Coming home past curfew is unacceptable for your safety. How can we make sure it doesn't happen next time?"
        }

    for key, val in library.items():
        if key in phrase:
            return val
    return "Try focusing on the boundary while offering a path forward with grace."

# --- STREAMLIT UI ---

st.set_page_config(page_title="Project Guardian 360", page_icon="🛡️")

# Sidebar for Family Personalization
st.sidebar.title("🛡️ Family Profile")
parent_role = st.sidebar.text_input("Your Role (e.g. Mom/Dad)", "Parent")
partner_name = st.sidebar.text_input("Partner/Co-Parent Name", "Partner")

st.sidebar.divider()
st.sidebar.header("The Grace Filter")
grace_level = st.sidebar.select_slider(
    "Child's Emotional State",
    options=["Calm", "Tired", "Stressed", "Meltdown"]
)

# Main Dashboard Header
st.title("Project Guardian 360")
st.caption(f"Logged in as: {parent_role} | Unified Front with: {partner_name}")

if grace_level == "Meltdown":
    st.error("🚨 **GRACE ALERT:** The child is over-stimulated. High firmness will likely escalate the situation. Prioritize safety and calm breathing first.")

tabs = st.tabs(["Direct Response", "Accountability", "Unified Front", "Hard Truths"])

with tabs[0]:
    st.header("Quick Rephrase")
    age = st.radio("Age Group", ["Child", "Teen"], horizontal=True)
    user_input = st.text_input("What are you about to say?", placeholder="e.g., Stop running!")
    
    if user_input:
        suggestion = get_rephrase(user_input, age)
        st.subheader("Try saying:")
        st.success(suggestion)

with tabs[1]:
    st.header("Parental Accountability")
    st.info("Model a well-adjusted adult by repairing the relationship.")
    if st.button("I lost my cool"):
        st.write(f"**Your Script:** 'I'm sorry I raised my voice. I was feeling frustrated, but that isn't an excuse. Can we try again?'")

with tabs[2]:
    st.header("The Unified Front")
    option = st.selectbox("Situation", ["Child asking for a 'Yes' after a 'No'", "Disagreement with Partner"])
    if option == "Child asking for a 'Yes' after a 'No'":
        st.warning(f"**Unified Move:** '{partner_name} already gave you an answer, and I support that. We are a team.')")
    else:
        st.info(f"**Grace Move:** Support {partner_name} in front of the child now. Discuss your different view in private later.")

with tabs[3]:
    st.header("Guardian Knowledge Base")
    st.markdown("""
    ### ⚓ Principles of the Anchor
    - **No Sugar-Coating:** Clarity is kindness. Being vague is confusing.
    - **Natural Consequences:** Let life teach the lessons that words cannot.
    - **Non-Binary Thinking:** You can be 100% firm on the rule and 100% soft on the person.
    """)

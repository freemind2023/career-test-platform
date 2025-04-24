import streamlit as st
from questions import questions
import matplotlib.pyplot as plt

st.set_page_config(page_title="Career Test | Practical EduSkills", layout="centered")

# 🔷 Custom Title & Subtitle
st.markdown("""
    <h1 style='text-align: center; font-size: 40px; color: #003366;'>
        Practical EduSkills
    </h1>
    <h3 style='text-align: center; font-size: 22px; color: #444444;'>
        AI-Based Roadmap Determiner for Practical B.Com and Practical BBA
    </h3>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Student Info ---
st.markdown("### 👤 Student Information")
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")

if name and phone:
    st.markdown("---")
    st.header("🧠 Personality Test")

    responses = []
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        response = st.radio("", list(q["options"].keys()), key=f"q_{i}")
        responses.append(q["options"][response])

    if st.button("📊 Submit Test"):
        bcom_score = responses.count("B.Com")
        bba_score = responses.count("BBA")

        st.success(f"Thanks, {name}! Here are your results:")
        st.markdown(f"📞 **Phone**: `{phone}`")
        st.markdown("---")

        # --- Result Recommendation ---
        if bcom_score > bba_score:
            st.markdown("🎯 **You are best suited for Practical B.Com.**")
            st.info("You have strong analytical skills, attention to detail, and enjoy working with data and finance.")
        elif bba_score > bcom_score:
            st.markdown("🎯 **You are best suited for Practical BBA.**")
            st.info("You have great leadership, communication, and organizational skills — ideal for business and management.")
        else:
            st.markdown("🎯 **You have a balanced personality. Both streams are worth exploring!**")

        # --- Score Breakdown ---
        st.markdown("### 📈 Score Breakdown")
        st.write(f"- B.Com Score: {bcom_score}")
        st.write(f"- BBA Score: {bba_score}")

        # --- Bar Chart Visualization ---
        st.markdown("### 📊 Visual Score Chart")

        labels = ['B.Com', 'BBA']
        scores = [bcom_score, bba_score]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, scores, color=['#003366', '#F39C12'])
        ax.set_ylabel('Score')
        ax.set_title('Career Fit Comparison')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, yval, ha='center', va='bottom')

        st.pyplot(fig)

else:
    st.warning("Please fill in your name and phone number to begin the test.")

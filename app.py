import streamlit as st
from questions import questions
import matplotlib.pyplot as plt
from xhtml2pdf import pisa
import tempfile
from io import BytesIO
import os

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
            result = "Practical B.Com"
            message = "You have strong analytical skills, attention to detail, and enjoy working with data and finance."
        elif bba_score > bcom_score:
            result = "Practical BBA"
            message = "You have great leadership, communication, and organizational skills — ideal for business and management."
        else:
            result = "Balanced Fit"
            message = "You have a balanced personality. Both streams are worth exploring!"

        st.markdown(f"🎯 **You are best suited for {result}.**")
        st.info(message)

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

        # --- PDF Generation ---
        def generate_pdf(name, phone, result, message, fig):
            # Save chart image
            chart_path = os.path.join(tempfile.gettempdir(), "chart.png")
            fig.savefig(chart_path)

            # Load and fill HTML template
            with open("report_template.html", "r") as f:
                html_template = f.read()

            html_filled = html_template.replace("{{ name }}", name)\
                                       .replace("{{ phone }}", phone)\
                                       .replace("{{ result }}", result)\
                                       .replace("{{ message }}", message)

            pdf_path = os.path.join(tempfile.gettempdir(), f"{name}_career_report.pdf")
            with open(pdf_path, "w+b") as result_file:
                pisa.CreatePDF(BytesIO(html_filled.encode("utf-8")), dest=result_file)

            return pdf_path

        pdf_file_path = generate_pdf(name, phone, result, message, fig)

        # --- Download Button ---
        with open(pdf_file_path, "rb") as f:
            st.download_button(
                label="📥 Download Career Report (PDF)",
                data=f,
                file_name=f"{name}_Career_Report.pdf",
                mime="application/pdf"
            )

else:
    st.warning("Please fill in your name and phone number to begin the test.")

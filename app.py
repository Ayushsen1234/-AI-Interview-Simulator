import streamlit as st
from fpdf import FPDF

questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "What is your biggest weakness?",
    "Where do you see yourself in 5 years?",
    "Why do you want to join our company?",
    "What are your career goals?",
    "Describe a challenging situation you faced.",
    "What programming languages do you know?",
    "Tell me about one of your projects."
]

st.title("🎤 AI Interview Simulator")

name = st.text_input("Enter Your Name")

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

progress = st.session_state.q_index / len(questions)
st.progress(progress)

if st.session_state.q_index < len(questions):

    st.write(
        f"### Question {st.session_state.q_index + 1} of {len(questions)}"
    )

    st.write(questions[st.session_state.q_index])

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        if len(answer) > 100:
            st.session_state.score += 10
        elif len(answer) > 50:
            st.session_state.score += 5
        else:
            st.session_state.score += 2

        st.session_state.q_index += 1
        st.rerun()

else:

    st.success("🎉 Interview Completed!")

    percentage = (st.session_state.score / 100) * 100

    st.write("### Final Result")
    st.write("👤 Name:", name)
    st.write("📊 Score:", st.session_state.score)
    st.write("📈 Percentage:", f"{percentage:.0f}%")

    if percentage >= 80:
        feedback = "Excellent communication skills. Keep it up!"
        st.success(feedback)

    elif percentage >= 50:
        feedback = "Good performance. Add more detailed answers."
        st.warning(feedback)

    else:
        feedback = "Practice more and improve your confidence."
        st.error(feedback)

    # PDF REPORT
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="AI Interview Report", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Candidate Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Score: {st.session_state.score}", ln=True)
    pdf.cell(200, 10, txt=f"Percentage: {percentage:.0f}%", ln=True)
    pdf.cell(200, 10, txt=f"Feedback: {feedback}", ln=True)

    pdf.output("Interview_Report.pdf")

    with open("Interview_Report.pdf", "rb") as file:
        st.download_button(
            label="📄 Download Interview Report",
            data=file,
            file_name="Interview_Report.pdf",
            mime="application/pdf"
        )

    if st.button("🔄 Restart Interview"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()
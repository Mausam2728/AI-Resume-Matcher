import streamlit as st
import sys
import os

# Backend logic ko import karne ke liye path set karna
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Aapke existing backend modules ko direct import karna
from backend.utils.parser import extract_text_from_pdf, extract_text_from_docx
from backend.utils.matcher import calculate_match_score

st.title("💼 AI Resume & Job Matcher")
st.write("Apna Resume upload karein aur Job Description paste karke Score check karein!")

jd_input = st.text_area("1. Job Description (JD) yahan paste karein:", height=200)
uploaded_file = st.file_uploader("2. Apna Resume upload karein (PDF/DOCX):", type=["pdf", "docx"])

if st.button("Check Match Score 🚀"):
    if not jd_input or not uploaded_file:
        st.error("Kripya dono cheezein (JD aur Resume) fill karein!")
    else:
        with st.spinner("AI analyze kar raha hai..."):
            temp_filename = ""
            try:
                file_ext = uploaded_file.name.split('.')[-1].lower()
                
                # File ko temporary save karna taaki parser ko sahi path mile
                temp_filename = f"temp_resume.{file_ext}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Functions me temporary file ka path pass karenge
                if file_ext == "pdf":
                    resume_text = extract_text_from_pdf(temp_filename)
                elif file_ext == "docx":
                    resume_text = extract_text_from_docx(temp_filename)
                else:
                    st.error("Unsupported file format!")
                    st.stop()

                # Match score nikalna
                score = calculate_match_score(resume_text, jd_input)
                
                # Temporary file ko delete karna kaam hone ke baad
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                
                # Result show karna
                st.success("Analysis Complete!")
                st.metric(label="ATS Match Score", value=f"{score}%")
                
            except Exception as e:
                # Agar koi error aaye tab bhi temp file delete ho jaye
                if temp_filename and os.path.exists(temp_filename):
                    os.remove(temp_filename)
                st.error(f"Kuch error aaya: {str(e)}")
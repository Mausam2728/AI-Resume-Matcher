import streamlit as st
import sys
import os

# Backend logic ko import karne ke liye path set karna
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Aapke existing backend modules ko direct import karna
from backend.utils.parser import extract_text_from_pdf, extract_text_from_docx  # check kar lena aapke functions ka naam yahi hai na
from backend.utils.matcher import calculate_match_score  # check kar lena function name

st.title("💼 AI Resume & Job Matcher")
st.write("Apna Resume upload karein aur Job Description paste karke Score check karein!")

jd_input = st.text_area("1. Job Description (JD) yahan paste karein:", height=200)
uploaded_file = st.file_uploader("2. Apna Resume upload karein (PDF/DOCX):", type=["pdf", "docx"])

if st.button("Check Match Score 🚀"):
    if not jd_input or not uploaded_file:
        st.error("Kripya dono cheezein (JD aur Resume) fill karein!")
    else:
        with st.spinner("AI analyze kar raha hai..."):
            try:
                # 1. File type check karke text extract karna
                file_ext = uploaded_file.name.split('.')[-1].lower()
                
                # Temporary file save karna ya bytes read karna aapke function ke mutabik
                file_bytes = uploaded_file.read()
                
                # NOTE: Agar aapke parser functions direct bytes lete hain to file_bytes bhejein,
                # agar wo path lete hain to hume temporary save karna padega. 
                # Maan lete hain wo direct file object ya bytes handle kar sakte hain:
                if file_ext == "pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif file_ext == "docx":
                    resume_text = extract_text_from_docx(uploaded_file)
                else:
                    st.error("Unsupported file format!")
                    st.stop()

                # 2. Match score calculate karna (Direct function call, No API needed!)
                # Aapke matcher function ke arguments ke hisab se ise check kar lena:
                score = calculate_match_score(resume_text, jd_input)
                
                # 3. Output show karna
                st.success("Analysis Complete!")
                st.metric(label="ATS Match Score", value=f"{score}%")
                
            except Exception as e:
                st.error(f"Kuch error aaya: {str(e)}")
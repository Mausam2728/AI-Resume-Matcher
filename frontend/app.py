import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Matcher", page_icon="💼")

st.title("💼 AI Resume & Job Matcher")
st.write("Apna Resume upload karein aur Job Description paste karke Score check karein!")

# User se inputs lena
jd_input = st.text_area("1. Job Description (JD) yahan paste karein:", height=200)
uploaded_file = st.file_uploader("2. Apna Resume upload karein (PDF/DOCX):", type=["pdf", "docx"])

if st.button("Check Match Score 🚀"):
    if not jd_input or not uploaded_file:
        st.error("Kripya dono cheezein (JD aur Resume) fill karein!")
    else:
        with st.spinner("AI analyze kar raha hai..."):
            # Backend server ka URL jahan data bhejna hai
            url = "http://127.0.0.1:8000/match"
            
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"jd": jd_input}
            
            try:
                # Backend ko request bhejna
                response = requests.post(url, files=files, data=data)
                result = response.json()
                
                if result.get("status") == "success":
                    score = result["match_percentage"]
                    st.success("Analysis Complete!")
                    st.metric(label="ATS Match Score", value=f"{score}%")
                    
                    if score >= 70:
                        st.balloons()
                        st.success("Boht badhiya match hai! Aap apply kar sakte hain.")
                    else:
                        st.warning("Score thoda kam hai. Resume me thode aur keywords add karein.")
                else:
                    st.error(result.get("message"))
            except Exception as e:
                st.error("Backend server se connect nahi ho pa raha. Kya apne server start kiya?")
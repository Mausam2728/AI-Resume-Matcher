with st.spinner("AI analyze kar raha hai..."):
            try:
                file_ext = uploaded_file.name.split('.')[-1].lower()
                
                # --- FIX: File ko temporary save karna taaki parser ko sahi path mile ---
                temp_filename = f"temp_resume.{file_ext}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Ab functions me temporary file ka path pass karenge
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
                # Agar error aaye tab bhi temp file delete ho jaye
                if 'temp_filename' in locals() and os.path.exists(temp_filename):
                    os.remove(temp_filename)
                st.error(f"Kuch error aaya: {str(e)}")
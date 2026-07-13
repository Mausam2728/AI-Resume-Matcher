from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from backend.utils.parser import parse_resume
from backend.utils.matcher import calculate_match_score

app = FastAPI(title="AI Resume Matcher API")

@app.post("/match")
async def match_resume_to_jd(
    jd: str = Form(...), 
    file: UploadFile = File(...)
):
    # Jo file user ne upload ki hai, uska extension check karna (.pdf ya .docx)
    file_ext = os.path.splitext(file.filename)[1].lower()
    temp_file_path = f"temp_resume{file_ext}"
    
    # File ko temporary save karna taaki hum use read kar sakein
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. Resume se text alag karo
        resume_text = parse_resume(temp_file_path, file_ext)
        
        # 2. AI model se match score nikalo
        score = calculate_match_score(resume_text, jd)
        
        return {
            "status": "success",
            "match_percentage": score
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
    finally:
        # Kaam khatam hone ke baad temporary file delete karna
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
import os
from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Yeni yazdığımız 20 alanlık fonksiyonları içeri aktarıyoruz
from services.interview import (
    compute_ai_ats_score,
    generate_first_question,
    generate_followup_question,
    evaluate_answer,
    generate_report
)

app = FastAPI(title="AI ATS & 20 IT Career Roadmap")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Klasör yolu hatasını engellemek için dinamik arama yapıyoruz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "templates")

# Eğer backend/templates yoksa, bir üst klasördeki templates'e bak emniyeti
if not os.path.exists(templates_dir):
    templates_dir = os.path.join(os.path.dirname(BASE_DIR), "templates")

templates = Jinja2Templates(directory=templates_dir)
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Ana sayfa yükleme rotası - Yeni standart dizilim"""
    return templates.TemplateResponse(request=request, name="index.html")
@app.post("/start_interview")
async def start_interview(domain: str = Form(...), cv_text: str = Form(None)):
    """Butonlara tıklandığında yol haritasını döner ve Gemini ile anlık canlı sorular üretir"""
    try:
        from services.interview import generate_first_question, get_interview_questions_from_ai
        
        # 1. Hazır olan akademik 4 haftalık yol haritasını çekiyoruz
        roadmap_content = generate_first_question(domain, cv_text or "")
        
        # 2. Canlı soruları Gemini motorundan fırlatıyoruz!
        interview_qs = get_interview_questions_from_ai(domain)
        
        return {
            "question": roadmap_content,
            "interview_questions": interview_qs
        }
    except Exception as e:
        return {"question": f"⚠️ Bir hata oluştu: {str(e)}", "interview_questions": []}

@app.post("/upload_cv")
async def upload_cv(file: UploadFile = File(...), domain: str = Form(...)):
    """İsteğe bağlı ATS analizi butonuna basıldığında çalışan rota"""
    try:
        contents = await file.read()
        cv_text = contents.decode("utf-8", errors="ignore")
        
        score, missing_keywords = compute_ai_ats_score(cv_text, domain)
        return {
            "score": score,
            "missing_keywords": missing_keywords,
            "status": "success"
        }
    except Exception as e:
        return {"score": 0, "missing_keywords": ["Dosya okunamadı"], "status": "error"}

@app.post("/get_report")
async def get_report(conversation: str = Form(...), domain: str = Form(...)):
    """Finaldeki resmi İK Raporunu getiren rota"""
    try:
        report_content = generate_report(conversation, domain)
        return {"report": report_content}
    except Exception as e:
        return {"report": f"Rapor oluşturulamadı: {str(e)}"}
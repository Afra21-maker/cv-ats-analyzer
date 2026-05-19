from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from .database import engine, get_db
from .models import Base
from .schemas import CandidateCreate, AnswerIn
from .repository import (
    get_candidate,
    create_candidate,
    create_cv,
    get_latest_cv,
    create_interview,
    get_interview,
    save_interview,
)
from .services.cv_parser import parse_cv
from .services.ats import compute_ats_score
from .services.interview import (
    generate_first_question,
    generate_followup_question,
    evaluate_answer,
    generate_report,
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_index():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.post("/api/candidates")
def api_create_candidate(input: CandidateCreate, db: Session = Depends(get_db)):
    candidate = create_candidate(db, input.name, input.email, input.domain)
    return {"id": candidate.id, "name": candidate.name, "domain": candidate.domain}

@app.post("/api/upload-cv")
def upload_cv(candidate_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı.")
    filename = file.filename
    target_path = UPLOAD_DIR / filename
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        text = parse_cv(str(target_path), filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    score, missing = compute_ats_score(text, candidate.domain)
    cv = create_cv(
        db,
        candidate.id,
        filename,
        text,
        score,
        candidate.domain,
        ", ".join(missing),
    )
    return {"candidate_id": cv.candidate_id, "filename": cv.filename, "score": cv.score, "missing_keywords": missing}

@app.post("/api/interview/start")
def start_interview(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı.")
    cv = get_latest_cv(db, candidate.id)
    if not cv:
        raise HTTPException(status_code=400, detail="CV yüklenmemiş.")
    question = generate_first_question(candidate.domain, cv.text)
    session = create_interview(db, candidate.id, candidate.domain, question)
    return {"interview_id": session.id, "question": question, "status": session.status}

@app.post("/api/interview/answer")
def answer_interview(payload: AnswerIn, db: Session = Depends(get_db)):
    session = get_interview(db, payload.interview_id)
    if not session:
        raise HTTPException(status_code=404, detail="Mülakat oturumu bulunamadı.")
    cv = get_latest_cv(db, session.candidate_id)
    if not cv:
        raise HTTPException(status_code=400, detail="CV yok.")
    feedback = evaluate_answer(payload.answer, session.last_question, cv.text)
    followup = generate_followup_question(session.domain, cv.text, session.conversation, payload.answer)
    session.conversation += f"CEVAP: {payload.answer}\nDEĞERLENDİRME: {feedback}\nSORU: {followup}\n"
    session.last_question = followup
    save_interview(db, session)
    return {"interview_id": session.id, "feedback": feedback, "next_question": followup}

@app.get("/api/report/{interview_id}")
def get_report(interview_id: int, db: Session = Depends(get_db)):
    session = get_interview(db, interview_id)
    if not session:
        raise HTTPException(status_code=404, detail="Mülakat oturumu bulunamadı.")
    if not session.report:
        session.report = generate_report(session.conversation, session.domain)
        save_interview(db, session)
    return {"interview_id": session.id, "report": session.report}

from sqlalchemy.orm import Session
from models import Candidate, CvUpload, InterviewSession

def get_candidate(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def create_candidate(db: Session, name: str, email: str | None, domain: str):
    candidate = Candidate(name=name, email=email, domain=domain)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def create_cv(db: Session, candidate_id: int, filename: str, text: str, score: int, domain: str, missing_keywords: str):
    cv = CvUpload(
        candidate_id=candidate_id,
        filename=filename,
        text=text,
        score=score,
        domain=domain,
        missing_keywords=missing_keywords,
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv

def get_latest_cv(db: Session, candidate_id: int):
    return (
        db.query(CvUpload)
        .filter(CvUpload.candidate_id == candidate_id)
        .order_by(CvUpload.id.desc())
        .first()
    )

def create_interview(db: Session, candidate_id: int, domain: str, question: str):
    session = InterviewSession(
        candidate_id=candidate_id,
        domain=domain,
        conversation=f"SORU: {question}\n",
        last_question=question,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_interview(db: Session, interview_id: int):
    return db.query(InterviewSession).filter(InterviewSession.id == interview_id).first()

def save_interview(db: Session, session: InterviewSession):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

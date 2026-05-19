from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    domain = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cvs = relationship("CvUpload", back_populates="candidate")
    interviews = relationship("InterviewSession", back_populates="candidate")

class CvUpload(Base):
    __tablename__ = "cv_uploads"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    filename = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    domain = Column(String, nullable=False)
    missing_keywords = Column(Text, nullable=True)
    candidate = relationship("Candidate", back_populates="cvs")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    domain = Column(String, nullable=False)
    status = Column(String, default="active")
    conversation = Column(Text, default="")
    last_question = Column(Text, default="")
    report = Column(Text, nullable=True)
    candidate = relationship("Candidate", back_populates="interviews")
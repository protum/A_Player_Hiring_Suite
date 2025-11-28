"""Interview models for biographical interviewing."""

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import uuid


class Interview(Base):
    """Interview session with a candidate."""

    __tablename__ = "interviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    scorecard_id = Column(String, ForeignKey("scorecards.id"))
    interview_date = Column(DateTime)
    interviewer_name = Column(String)
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    overall_rating = Column(String)  # A, B, C
    hire_recommendation = Column(Boolean)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    job_history = relationship("JobHistory", back_populates="interview", cascade="all, delete-orphan")
    red_flags = relationship("RedFlag", back_populates="interview", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Interview {self.id} - Candidate {self.candidate_id}>"


class JobHistory(Base):
    """Work history entry for a candidate."""

    __tablename__ = "job_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    sequence_order = Column(Integer)
    responsibilities = Column(Text)

    # Relationships
    interview = relationship("Interview", back_populates="job_history")
    questions = relationship("InterviewQuestion", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobHistory: {self.title} at {self.company}>"


class InterviewQuestion(Base):
    """Questions and responses during interview."""

    __tablename__ = "interview_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_history_id = Column(String, ForeignKey("job_history.id", ondelete="CASCADE"), nullable=False)
    question_type = Column(String, nullable=False)  # accomplishment, mistake, boss_rating, reason_leaving, etc.
    question_text = Column(Text, nullable=False)
    response = Column(Text)
    rating = Column(Integer)  # 1-5
    notes = Column(Text)

    # Relationships
    job = relationship("JobHistory", back_populates="questions")

    def __repr__(self):
        return f"<Question: {self.question_type}>"


class RedFlag(Base):
    """Red flags identified during interview."""

    __tablename__ = "red_flags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    flag_type = Column(String, nullable=False)  # consistency, evasion, negative_pattern, reference_concern
    description = Column(Text, nullable=False)
    severity = Column(String)  # low, medium, high
    job_history_id = Column(String, ForeignKey("job_history.id"))
    created_at = Column(DateTime, default=func.now())

    # Relationships
    interview = relationship("Interview", back_populates="red_flags")

    def __repr__(self):
        return f"<RedFlag: {self.flag_type} - {self.severity}>"

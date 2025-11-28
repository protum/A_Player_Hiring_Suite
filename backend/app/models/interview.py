"""
Topgrading Interview models
Chronological in-depth structured interview
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Text, Integer, DateTime, Date, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class InterviewStatus(str, enum.Enum):
    """Interview status enumeration"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InterviewRecommendation(str, enum.Enum):
    """Interview recommendation enumeration"""
    STRONG_YES = "strong_yes"
    YES = "yes"
    MAYBE = "maybe"
    NO = "no"
    STRONG_NO = "strong_no"


class RedFlagSeverity(str, enum.Enum):
    """Red flag severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Interview(Base):
    """
    Topgrading Interview model
    Chronological in-depth structured interview
    """
    __tablename__ = "interviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_name = Column(String(255), nullable=False)
    candidate_email = Column(String(255))
    interviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    scorecard_id = Column(UUID(as_uuid=True), ForeignKey("scorecards.id", ondelete="SET NULL"))
    interview_date = Column(DateTime)
    status = Column(Enum(InterviewStatus), default=InterviewStatus.SCHEDULED, nullable=False)
    overall_rating = Column(Numeric(3, 2))  # 0.00 to 5.00
    cqi_score = Column(Integer)  # Candidate Quality Index: 0-100
    recommendation = Column(Enum(InterviewRecommendation))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    interviewer = relationship("User", back_populates="interviews_conducted", foreign_keys=[interviewer_id])
    scorecard = relationship("Scorecard", back_populates="interviews")
    career_blocks = relationship("InterviewCareerBlock", back_populates="interview", cascade="all, delete-orphan")
    red_flags = relationship("RedFlag", back_populates="interview", cascade="all, delete-orphan")
    reference_checks = relationship("ReferenceCheck", back_populates="interview", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Interview {self.candidate_name}>"


class InterviewCareerBlock(Base):
    """
    Career block within an interview
    Chronological work history segment
    """
    __tablename__ = "interview_career_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(255), nullable=False)
    role_title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    achievements = Column(JSONB, default=list)  # List of achievements
    failures = Column(JSONB, default=list)  # List of failures/challenges
    boss_name = Column(String(255))
    boss_rating = Column(Integer)  # 1-10 scale - how candidate thinks boss would rate them
    reason_for_leaving = Column(Text)
    order_index = Column(Integer, default=0)  # To maintain chronological order
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    interview = relationship("Interview", back_populates="career_blocks")
    boss_ratings = relationship("BossRating", back_populates="career_block", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InterviewCareerBlock {self.company_name} - {self.role_title}>"


class BossRating(Base):
    """
    Boss rating for a career block
    TORC (Threat of Reference Check) - candidate predicts boss's rating
    """
    __tablename__ = "boss_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_block_id = Column(UUID(as_uuid=True), ForeignKey("interview_career_blocks.id", ondelete="CASCADE"), nullable=False)
    predicted_rating = Column(Integer, nullable=False)  # 1-10 scale
    actual_rating = Column(Integer)  # 1-10 scale (from reference check)
    boss_strengths_feedback = Column(Text)  # What boss would say as strengths
    boss_weaknesses_feedback = Column(Text)  # What boss would say as weaknesses
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    career_block = relationship("InterviewCareerBlock", back_populates="boss_ratings")

    def __repr__(self):
        return f"<BossRating predicted={self.predicted_rating}>"


class RedFlag(Base):
    """
    Red flags detected during interview
    Automatic and manual detection
    """
    __tablename__ = "red_flags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    flag_type = Column(String(100), nullable=False)  # e.g., "job_hopping", "vague_answers", "blame_others"
    severity = Column(Enum(RedFlagSeverity), default=RedFlagSeverity.MEDIUM, nullable=False)
    description = Column(Text, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_resolved = Column(String(10), default="false")  # "false" or explanation
    auto_detected = Column(String(10), default="false")  # "true" if detected by algorithm

    # Relationships
    interview = relationship("Interview", back_populates="red_flags")

    def __repr__(self):
        return f"<RedFlag {self.flag_type} - {self.severity}>"


class ReferenceCheck(Base):
    """
    Reference check record
    Follow-up to TORC predictions
    """
    __tablename__ = "reference_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    reference_name = Column(String(255), nullable=False)
    reference_title = Column(String(255))
    reference_company = Column(String(255))
    reference_email = Column(String(255))
    reference_phone = Column(String(50))
    relationship_to_candidate = Column(String(100))
    actual_rating = Column(Integer)  # 1-10 scale
    strengths_mentioned = Column(Text)
    weaknesses_mentioned = Column(Text)
    would_rehire = Column(String(10))  # "yes", "no", "maybe"
    notes = Column(Text)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    interview = relationship("Interview", back_populates="reference_checks")

    def __repr__(self):
        return f"<ReferenceCheck {self.reference_name}>"

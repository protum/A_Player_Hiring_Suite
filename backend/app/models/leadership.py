"""
Leadership Assessment models (CEO Next Door - 4 Behaviors)
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class AssessmentStatus(str, enum.Enum):
    """Assessment status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class BehaviorType(str, enum.Enum):
    """CEO Behavior type enumeration (The CEO Next Door)"""
    DECISIVENESS = "decisiveness"
    RELIABILITY = "reliability"
    BOLD_ADAPTATION = "bold_adaptation"
    ENGAGING_IMPACT = "engaging_impact"


class LeadershipAssessment(Base):
    """
    Leadership Assessment model
    360-degree assessment of the 4 CEO behaviors
    """
    __tablename__ = "leadership_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_period = Column(String(50), nullable=False)  # e.g., "Q1 2025"
    status = Column(Enum(AssessmentStatus), default=AssessmentStatus.PENDING, nullable=False)

    # Aggregate scores for the 4 behaviors (calculated from ratings)
    decisiveness_score = Column(Numeric(4, 2))  # 0.00 to 10.00
    reliability_score = Column(Numeric(4, 2))
    bold_adaptation_score = Column(Numeric(4, 2))
    engaging_impact_score = Column(Numeric(4, 2))
    overall_score = Column(Numeric(4, 2))

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    subject = relationship("User", back_populates="leadership_assessments_subject", foreign_keys=[subject_id])
    behavior_ratings = relationship("BehaviorRating", back_populates="assessment", cascade="all, delete-orphan")
    evidence_items = relationship("EvidenceItem", back_populates="assessment", cascade="all, delete-orphan")
    development_plans = relationship("DevelopmentPlan", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LeadershipAssessment {self.assessment_period}>"


class BehaviorRating(Base):
    """
    Individual behavior rating from a rater
    Part of 360-degree assessment
    """
    __tablename__ = "behavior_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("leadership_assessments.id", ondelete="CASCADE"), nullable=False)
    rater_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    behavior_type = Column(Enum(BehaviorType), nullable=False)
    dimension = Column(String(100), nullable=False)  # Specific dimension of the behavior
    score = Column(Integer, nullable=False)  # 0-10 scale
    evidence = Column(Text)  # Specific examples/evidence
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("LeadershipAssessment", back_populates="behavior_ratings")

    def __repr__(self):
        return f"<BehaviorRating {self.behavior_type} - {self.score}>"


class Rater(Base):
    """
    Rater in a 360-degree assessment
    Can be peer, direct report, manager, board member, etc.
    """
    __tablename__ = "raters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("leadership_assessments.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    relationship_type = Column(String(100), nullable=False)  # e.g., "peer", "direct_report", "manager"
    has_submitted = Column(String(10), default="false")  # "true" or "false"
    invited_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime)

    def __repr__(self):
        return f"<Rater {self.name} - {self.relationship_type}>"


class EvidenceItem(Base):
    """
    Evidence item for a behavior
    Specific examples of behavior in action
    """
    __tablename__ = "evidence_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("leadership_assessments.id", ondelete="CASCADE"), nullable=False)
    behavior_type = Column(Enum(BehaviorType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    impact = Column(Text)
    date_occurred = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("LeadershipAssessment", back_populates="evidence_items")

    def __repr__(self):
        return f"<EvidenceItem {self.title}>"


class DevelopmentPlan(Base):
    """
    Leadership development plan
    Action items to improve specific behaviors
    """
    __tablename__ = "development_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("leadership_assessments.id", ondelete="CASCADE"), nullable=False)
    behavior_type = Column(Enum(BehaviorType), nullable=False)
    goal = Column(String(255), nullable=False)
    action_items = Column(JSONB, default=list)  # List of specific actions
    success_metrics = Column(JSONB, default=list)  # How to measure success
    timeline = Column(String(100))
    status = Column(String(50), default="not_started")  # "not_started", "in_progress", "completed"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("LeadershipAssessment", back_populates="development_plans")

    def __repr__(self):
        return f"<DevelopmentPlan {self.goal}>"

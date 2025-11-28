"""Assessment models for CEO Behaviors and Power Score."""

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import uuid


class CEOAssessment(Base):
    """CEO Behaviors assessment based on 'The CEO Next Door'."""

    __tablename__ = "ceo_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    assessment_type = Column(String, nullable=False)  # self, observer, 360
    assessor_name = Column(String)
    overall_score = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    behavior_ratings = relationship("CEOBehaviorRating", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CEOAssessment {self.id} - {self.assessment_type}>"


class CEOBehaviorRating(Base):
    """Individual behavior ratings within CEO assessment."""

    __tablename__ = "ceo_behavior_ratings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("ceo_assessments.id", ondelete="CASCADE"), nullable=False)
    behavior = Column(String, nullable=False)  # decisiveness, reliability, adaptation, engagement
    score = Column(Integer, nullable=False)  # 1-5
    evidence = Column(Text)
    development_notes = Column(Text)

    # Relationships
    assessment = relationship("CEOAssessment", back_populates="behavior_ratings")

    def __repr__(self):
        return f"<BehaviorRating: {self.behavior} - {self.score}>"


class PowerScoreAssessment(Base):
    """Power Score assessment for leadership evaluation."""

    __tablename__ = "power_score_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    results_score = Column(Float, nullable=False)
    relationships_score = Column(Float, nullable=False)
    role_model_score = Column(Float, nullable=False)
    overall_power_score = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    responses = relationship("PowerScoreResponse", back_populates="assessment", cascade="all, delete-orphan")
    development_plans = relationship("DevelopmentPlan", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PowerScore {self.overall_power_score:.1f} - Subject {self.subject_id}>"


class PowerScoreResponse(Base):
    """Individual question responses for Power Score assessment."""

    __tablename__ = "power_score_responses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("power_score_assessments.id", ondelete="CASCADE"), nullable=False)
    dimension = Column(String, nullable=False)  # results, relationships, role_model
    question_id = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    response_value = Column(Integer)  # 1-5 scale
    response_text = Column(Text)

    # Relationships
    assessment = relationship("PowerScoreAssessment", back_populates="responses")

    def __repr__(self):
        return f"<PowerScoreResponse: {self.dimension} - Q{self.question_id}>"


class DevelopmentPlan(Base):
    """Development plan items linked to Power Score assessment."""

    __tablename__ = "development_plans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("power_score_assessments.id", ondelete="CASCADE"), nullable=False)
    dimension = Column(String, nullable=False)  # results, relationships, role_model
    goal = Column(Text, nullable=False)
    action_steps = Column(Text)
    target_date = Column(Date)
    status = Column(String, default="active")  # active, completed, abandoned
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    assessment = relationship("PowerScoreAssessment", back_populates="development_plans")

    def __repr__(self):
        return f"<DevelopmentPlan: {self.goal[:50]}>"

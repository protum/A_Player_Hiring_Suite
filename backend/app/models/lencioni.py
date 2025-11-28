"""Ideal Team Player and Core Values assessment models."""

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import uuid


class IdealTeamPlayerAssessment(Base):
    """
    Ideal Team Player assessment based on Patrick Lencioni's framework.

    Assesses candidates across three core virtues:
    - Humble: Lacks excessive ego, shares credit
    - Hungry: Self-motivated, always looking to do more
    - Smart: People smart, good emotional intelligence
    """

    __tablename__ = "ideal_team_player_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    assessment_type = Column(String, nullable=False)  # self, observer, interview
    assessor_name = Column(String)

    # Virtue scores (1-5 scale)
    humble_score = Column(Float, nullable=False)
    hungry_score = Column(Float, nullable=False)
    smart_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)

    # Category based on virtues
    category = Column(String)  # ideal_team_player, humble_only, hungry_only, etc.

    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    virtue_ratings = relationship("IdealTeamPlayerVirtueRating", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<IdealTeamPlayerAssessment {self.id} - {self.category}>"


class IdealTeamPlayerVirtueRating(Base):
    """Detailed ratings for each virtue dimension."""

    __tablename__ = "ideal_team_player_virtue_ratings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("ideal_team_player_assessments.id", ondelete="CASCADE"), nullable=False)
    virtue = Column(String, nullable=False)  # humble, hungry, smart
    question_id = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    response_value = Column(Integer, nullable=False)  # 1-5 scale
    evidence = Column(Text)

    # Relationships
    assessment = relationship("IdealTeamPlayerAssessment", back_populates="virtue_ratings")

    def __repr__(self):
        return f"<VirtueRating: {self.virtue} - {self.response_value}>"


class CoreValuesAssessment(Base):
    """
    Core Values assessment aligned with organizational values:
    1. Personal Growth
    2. Harmonious Relationships
    3. Problem Solving
    4. Positive Impact
    5. Financial Stewardship
    """

    __tablename__ = "core_values_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    assessment_type = Column(String, nullable=False)  # interview, behavioral, reference
    assessor_name = Column(String)

    # Value scores (0-100 scale)
    personal_growth_score = Column(Float, nullable=False)
    harmonious_relationships_score = Column(Float, nullable=False)
    problem_solving_score = Column(Float, nullable=False)
    positive_impact_score = Column(Float, nullable=False)
    financial_stewardship_score = Column(Float, nullable=False)
    overall_alignment_score = Column(Float, nullable=False)

    # Alignment rating
    alignment_level = Column(String)  # strong_fit, good_fit, partial_fit, poor_fit

    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    value_ratings = relationship("CoreValueRating", back_populates="assessment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CoreValuesAssessment {self.id} - {self.alignment_level}>"


class CoreValueRating(Base):
    """Detailed ratings for each core value."""

    __tablename__ = "core_value_ratings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("core_values_assessments.id", ondelete="CASCADE"), nullable=False)
    value = Column(String, nullable=False)  # personal_growth, harmonious_relationships, etc.
    question_id = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    response_value = Column(Integer, nullable=False)  # 1-5 scale
    evidence = Column(Text)

    # Relationships
    assessment = relationship("CoreValuesAssessment", back_populates="value_ratings")

    def __repr__(self):
        return f"<ValueRating: {self.value} - {self.response_value}>"

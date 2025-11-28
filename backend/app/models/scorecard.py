"""Scorecard models for A-Method scorecards."""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import uuid


class Scorecard(Base):
    """Role scorecard based on 'Who: The A Method for Hiring'."""

    __tablename__ = "scorecards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role_title = Column(String, nullable=False)
    mission = Column(Text, nullable=False)
    department = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    outcomes = relationship("ScorecardOutcome", back_populates="scorecard", cascade="all, delete-orphan")
    competencies = relationship("ScorecardCompetency", back_populates="scorecard", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scorecard {self.role_title}>"


class ScorecardOutcome(Base):
    """Measurable outcomes for a scorecard."""

    __tablename__ = "scorecard_outcomes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scorecard_id = Column(String, ForeignKey("scorecards.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)
    metric = Column(String)
    timeframe = Column(String)
    priority = Column(Integer)

    # Relationships
    scorecard = relationship("Scorecard", back_populates="outcomes")

    def __repr__(self):
        return f"<Outcome: {self.description[:50]}>"


class ScorecardCompetency(Base):
    """Competencies required for a role."""

    __tablename__ = "scorecard_competencies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scorecard_id = Column(String, ForeignKey("scorecards.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    definition = Column(Text)

    # Relationships
    scorecard = relationship("Scorecard", back_populates="competencies")
    indicators = relationship("CompetencyIndicator", back_populates="competency", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Competency: {self.name}>"


class CompetencyIndicator(Base):
    """Behavioral indicators for a competency."""

    __tablename__ = "competency_indicators"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    competency_id = Column(String, ForeignKey("scorecard_competencies.id", ondelete="CASCADE"), nullable=False)
    indicator = Column(Text, nullable=False)

    # Relationships
    competency = relationship("ScorecardCompetency", back_populates="indicators")

    def __repr__(self):
        return f"<Indicator: {self.indicator[:50]}>"

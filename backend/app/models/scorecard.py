"""
A-Method Scorecard models (WHO framework)
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum, ForeignKey, JSON, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ScorecardStatus(str, enum.Enum):
    """Scorecard status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Scorecard(Base):
    """
    A-Method Scorecard model
    Defines mission, outcomes, and competencies for a role
    """
    __tablename__ = "scorecards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    role_title = Column(String(255), nullable=False)
    role_mission = Column(Text, nullable=False)
    status = Column(Enum(ScorecardStatus), default=ScorecardStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="scorecards")
    created_by = relationship("User", back_populates="scorecards_created", foreign_keys=[created_by_id])
    outcomes = relationship("ScorecardOutcome", back_populates="scorecard", cascade="all, delete-orphan")
    competencies = relationship("ScorecardCompetency", back_populates="scorecard", cascade="all, delete-orphan")
    versions = relationship("ScorecardVersion", back_populates="scorecard", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="scorecard")

    def __repr__(self):
        return f"<Scorecard {self.role_title}>"


class ScorecardOutcome(Base):
    """
    Measurable outcome for a scorecard
    3-5 outcomes per scorecard
    """
    __tablename__ = "scorecard_outcomes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scorecard_id = Column(UUID(as_uuid=True), ForeignKey("scorecards.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)
    metric = Column(String(255), nullable=False)
    target_value = Column(String(100), nullable=False)
    timeframe = Column(String(100), nullable=False)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scorecard = relationship("Scorecard", back_populates="outcomes")

    def __repr__(self):
        return f"<ScorecardOutcome {self.metric}>"


class ScorecardCompetency(Base):
    """
    Competency required for a role
    5-8 competencies per scorecard
    """
    __tablename__ = "scorecard_competencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scorecard_id = Column(UUID(as_uuid=True), ForeignKey("scorecards.id", ondelete="CASCADE"), nullable=False)
    competency_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    behavioral_anchors = Column(JSONB, default=dict)  # Examples of good/poor performance
    weight = Column(Numeric(3, 2), default=1.0)  # Weighting factor for importance
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scorecard = relationship("Scorecard", back_populates="competencies")

    def __repr__(self):
        return f"<ScorecardCompetency {self.competency_name}>"


class ScorecardVersion(Base):
    """
    Version history for scorecards
    Tracks changes over time
    """
    __tablename__ = "scorecard_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scorecard_id = Column(UUID(as_uuid=True), ForeignKey("scorecards.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    snapshot_data = Column(JSONB, nullable=False)  # Full scorecard data at this version
    changed_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    change_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scorecard = relationship("Scorecard", back_populates="versions")

    def __repr__(self):
        return f"<ScorecardVersion {self.version_number}>"

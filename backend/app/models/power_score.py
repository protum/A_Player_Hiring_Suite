"""
Power Score models (P × W × R formula)
Executive effectiveness assessment
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Text, Integer, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base


class PowerScore(Base):
    """
    Power Score model
    Formula: Total Power Score = Priorities (P) × Who (W) × Relationships (R)
    """
    __tablename__ = "power_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    executive_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_date = Column(Date, nullable=False, default=date.today)

    # Core dimensions (0.00 to 10.00 each)
    priorities_score = Column(Numeric(4, 2))  # P dimension
    who_score = Column(Numeric(4, 2))  # W dimension
    relationships_score = Column(Numeric(4, 2))  # R dimension

    # Total Power Score (P × W × R)
    total_power_score = Column(Numeric(8, 2))  # Can be up to 1000.00

    # Analysis
    weakest_dimension = Column(String(50))  # "priorities", "who", or "relationships"
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    executive = relationship("User", back_populates="power_scores", foreign_keys=[executive_id])
    priority_assessment = relationship(
        "PriorityAssessment",
        back_populates="power_score",
        uselist=False,
        cascade="all, delete-orphan"
    )
    who_assessment = relationship(
        "WhoAssessment",
        back_populates="power_score",
        uselist=False,
        cascade="all, delete-orphan"
    )
    relationship_assessment = relationship(
        "RelationshipAssessment",
        back_populates="power_score",
        uselist=False,
        cascade="all, delete-orphan"
    )
    improvement_plans = relationship("ImprovementPlan", back_populates="power_score", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PowerScore total={self.total_power_score}>"


class PriorityAssessment(Base):
    """
    Priorities (P) dimension assessment
    Measures clarity and focus on key priorities
    """
    __tablename__ = "priority_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_score_id = Column(UUID(as_uuid=True), ForeignKey("power_scores.id", ondelete="CASCADE"), nullable=False)

    # Sub-dimensions (0-10 each)
    clarity_score = Column(Integer, nullable=False)  # Clear definition of priorities
    focus_score = Column(Integer, nullable=False)  # Ability to maintain focus
    alignment_score = Column(Integer, nullable=False)  # Team alignment on priorities
    resource_consistency_score = Column(Integer, nullable=False)  # Resources match priorities

    # Average score
    average_score = Column(Numeric(4, 2))

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    power_score = relationship("PowerScore", back_populates="priority_assessment")

    def __repr__(self):
        return f"<PriorityAssessment avg={self.average_score}>"


class WhoAssessment(Base):
    """
    Who (W) dimension assessment
    Measures team quality and capability
    """
    __tablename__ = "who_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_score_id = Column(UUID(as_uuid=True), ForeignKey("power_scores.id", ondelete="CASCADE"), nullable=False)

    # Sub-dimensions (0-10 each)
    bench_strength_score = Column(Integer, nullable=False)  # Leadership bench strength
    a_player_ratio_score = Column(Integer, nullable=False)  # Percentage of A players
    team_gaps_score = Column(Integer, nullable=False)  # Inverse of critical gaps (10 = no gaps)
    delegation_efficiency_score = Column(Integer, nullable=False)  # Effective delegation

    # Average score
    average_score = Column(Numeric(4, 2))

    # Additional data
    total_team_size = Column(Integer)
    estimated_a_players = Column(Integer)
    critical_gaps = Column(JSONB, default=list)  # List of critical role gaps

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    power_score = relationship("PowerScore", back_populates="who_assessment")

    def __repr__(self):
        return f"<WhoAssessment avg={self.average_score}>"


class RelationshipAssessment(Base):
    """
    Relationships (R) dimension assessment
    Measures quality of key relationships
    """
    __tablename__ = "relationship_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_score_id = Column(UUID(as_uuid=True), ForeignKey("power_scores.id", ondelete="CASCADE"), nullable=False)

    # Sub-dimensions (0-10 each)
    board_alignment_score = Column(Integer, nullable=False)  # Board relationship quality
    cross_team_collaboration_score = Column(Integer, nullable=False)  # Cross-functional collaboration
    market_trust_score = Column(Integer, nullable=False)  # External stakeholder trust
    culture_health_score = Column(Integer, nullable=False)  # Organizational culture

    # Average score
    average_score = Column(Numeric(4, 2))

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    power_score = relationship("PowerScore", back_populates="relationship_assessment")

    def __repr__(self):
        return f"<RelationshipAssessment avg={self.average_score}>"


class ImprovementPlan(Base):
    """
    Power Score improvement plan
    Action items to strengthen weakest dimension
    """
    __tablename__ = "improvement_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_score_id = Column(UUID(as_uuid=True), ForeignKey("power_scores.id", ondelete="CASCADE"), nullable=False)
    target_dimension = Column(String(50), nullable=False)  # "priorities", "who", or "relationships"
    goal = Column(String(255), nullable=False)
    action_items = Column(JSONB, default=list)  # List of specific actions
    expected_impact = Column(Text)
    timeline = Column(String(100))
    status = Column(String(50), default="not_started")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    power_score = relationship("PowerScore", back_populates="improvement_plans")

    def __repr__(self):
        return f"<ImprovementPlan {self.target_dimension}>"

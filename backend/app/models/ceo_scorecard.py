"""
CEO Scorecard models
Comprehensive executive performance scorecard combining:
- CEO Next Door 4 Behaviors
- Power Score (P × W × R)
- CEO Operating Metrics
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class CEOScorecardStatus(str, enum.Enum):
    """CEO Scorecard status enumeration"""
    DRAFT = "draft"
    FINALIZED = "finalized"
    ARCHIVED = "archived"


class RecommendationType(str, enum.Enum):
    """Recommendation type enumeration"""
    BEHAVIOR_IMPROVEMENT = "behavior_improvement"
    POWER_SCORE_IMPROVEMENT = "power_score_improvement"
    FAILURE_POINT_MITIGATION = "failure_point_mitigation"


class RecommendationPriority(str, enum.Enum):
    """Recommendation priority enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CEOScorecard(Base):
    """
    CEO Scorecard model
    Comprehensive executive performance assessment
    """
    __tablename__ = "ceo_scorecards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ceo_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    period = Column(String(50), nullable=False)  # e.g., "Q1 2025"

    # CEO Excellence Index (0-100)
    # Composite score across all dimensions
    ceo_excellence_index = Column(Numeric(5, 2))

    status = Column(Enum(CEOScorecardStatus), default=CEOScorecardStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    finalized_at = Column(DateTime)

    # Relationships
    ceo = relationship("User", back_populates="ceo_scorecards", foreign_keys=[ceo_id])
    organization = relationship("Organization", back_populates="ceo_scorecards")
    behavior_scores = relationship("CEOBehaviorScore", back_populates="ceo_scorecard", cascade="all, delete-orphan")
    power_scores = relationship("CEOPowerScore", back_populates="ceo_scorecard", cascade="all, delete-orphan")
    operating_metrics = relationship("CEOOperatingMetrics", back_populates="ceo_scorecard", cascade="all, delete-orphan")
    recommendations = relationship("CEORecommendation", back_populates="ceo_scorecard", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CEOScorecard {self.period} - Index: {self.ceo_excellence_index}>"


class CEOBehaviorScore(Base):
    """
    CEO Next Door 4 Behaviors scores
    Each behavior broken into sub-dimensions
    """
    __tablename__ = "ceo_behavior_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ceo_scorecard_id = Column(UUID(as_uuid=True), ForeignKey("ceo_scorecards.id", ondelete="CASCADE"), nullable=False)

    # DECISIVENESS (0-10 each)
    decision_speed = Column(Integer)  # Speed of decision cycles
    decision_quality = Column(Integer)  # Quality of decision inputs
    loss_cutting = Column(Integer)  # Ability to cut losses
    ambiguity_handling = Column(Integer)  # Handling ambiguity

    # RELIABILITY (0-10 each)
    predictability = Column(Integer)  # Delivering predictably
    commitment_delivery = Column(Integer)  # Meeting commitments
    process_discipline = Column(Integer)  # Building repeatable processes
    time_management = Column(Integer)  # Time management & execution discipline

    # BOLD ADAPTATION (0-10 each)
    pivot_capacity = Column(Integer)  # Pivoting under pressure
    inflection_recognition = Column(Integer)  # Recognizing inflection points
    experimentation_velocity = Column(Integer)  # Experimentation velocity
    learning_agility = Column(Integer)  # Learning agility

    # ENGAGING FOR IMPACT (0-10 each)
    stakeholder_influence = Column(Integer)  # Stakeholder influence
    cross_functional_alignment = Column(Integer)  # Cross-functional alignment
    vision_communication = Column(Integer)  # Vision communication
    talent_magnetism = Column(Integer)  # Talent magnetism

    # Aggregate scores for each behavior (calculated average)
    decisiveness_score = Column(Numeric(4, 2))
    reliability_score = Column(Numeric(4, 2))
    bold_adaptation_score = Column(Numeric(4, 2))
    engaging_impact_score = Column(Numeric(4, 2))

    # Overall behavior score (average of 4 behaviors)
    overall_behavior_score = Column(Numeric(4, 2))

    # Analysis
    weakest_behavior = Column(String(50))  # Name of weakest behavior
    strongest_behavior = Column(String(50))  # Name of strongest behavior

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    ceo_scorecard = relationship("CEOScorecard", back_populates="behavior_scores")

    def __repr__(self):
        return f"<CEOBehaviorScore overall={self.overall_behavior_score}>"


class CEOPowerScore(Base):
    """
    Power Score (P × W × R) for CEO
    Each dimension with sub-components
    """
    __tablename__ = "ceo_power_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ceo_scorecard_id = Column(UUID(as_uuid=True), ForeignKey("ceo_scorecards.id", ondelete="CASCADE"), nullable=False)

    # PRIORITIES (P) - 0-10 each
    clarity_score = Column(Integer)
    focus_score = Column(Integer)
    alignment_score = Column(Integer)
    resource_consistency_score = Column(Integer)

    # WHO (W) - 0-10 each
    bench_strength_score = Column(Integer)
    a_player_ratio_score = Column(Integer)
    team_gaps_score = Column(Integer)
    delegation_efficiency_score = Column(Integer)

    # RELATIONSHIPS (R) - 0-10 each
    board_alignment_score = Column(Integer)
    cross_team_collaboration_score = Column(Integer)
    market_trust_score = Column(Integer)
    culture_health_score = Column(Integer)

    # Aggregate dimension scores (average of sub-components)
    priorities_score = Column(Numeric(4, 2))  # P
    who_score = Column(Numeric(4, 2))  # W
    relationships_score = Column(Numeric(4, 2))  # R

    # Total Power Score (P × W × R)
    total_power_score = Column(Numeric(8, 2))

    # Analysis
    weakest_dimension = Column(String(50))  # "priorities", "who", or "relationships"
    weakest_sub_component = Column(String(100))  # Specific weakest sub-component

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    ceo_scorecard = relationship("CEOScorecard", back_populates="power_scores")

    def __repr__(self):
        return f"<CEOPowerScore total={self.total_power_score}>"


class CEOOperatingMetrics(Base):
    """
    CEO Operating Metrics
    Quantitative performance indicators
    """
    __tablename__ = "ceo_operating_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ceo_scorecard_id = Column(UUID(as_uuid=True), ForeignKey("ceo_scorecards.id", ondelete="CASCADE"), nullable=False)

    # Operating metrics (0-100 each, percentage achievement)
    quarterly_goal_achievement = Column(Integer)  # % of quarterly goals achieved
    revenue_target_performance = Column(Integer)  # % of revenue target achieved
    cash_runway_discipline = Column(Integer)  # Cash management score
    strategy_execution_score = Column(Integer)  # Strategy execution effectiveness
    people_leadership_score = Column(Integer)  # People management effectiveness
    org_engagement_score = Column(Integer)  # Organization-wide engagement
    customer_impact_score = Column(Integer)  # Customer satisfaction/impact

    # Composite operating score (average)
    overall_operating_score = Column(Numeric(5, 2))

    # Additional context
    revenue_actual = Column(Numeric(15, 2))
    revenue_target = Column(Numeric(15, 2))
    cash_runway_months = Column(Numeric(4, 1))
    team_size = Column(Integer)
    customer_nps = Column(Integer)  # Net Promoter Score

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    ceo_scorecard = relationship("CEOScorecard", back_populates="operating_metrics")

    def __repr__(self):
        return f"<CEOOperatingMetrics overall={self.overall_operating_score}>"


class CEORecommendation(Base):
    """
    CEO development recommendations
    Based on scorecard analysis
    """
    __tablename__ = "ceo_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ceo_scorecard_id = Column(UUID(as_uuid=True), ForeignKey("ceo_scorecards.id", ondelete="CASCADE"), nullable=False)

    recommendation_type = Column(Enum(RecommendationType), nullable=False)
    priority = Column(Enum(RecommendationPriority), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    action_items = Column(JSONB, default=list)  # List of specific actions
    expected_impact = Column(Text)

    # Tracking
    status = Column(String(50), default="pending")  # "pending", "in_progress", "completed"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    ceo_scorecard = relationship("CEOScorecard", back_populates="recommendations")

    def __repr__(self):
        return f"<CEORecommendation {self.title} - {self.priority}>"

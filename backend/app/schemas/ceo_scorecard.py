"""
CEO Scorecard schemas
"""
from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict
from datetime import datetime
from app.models.ceo_scorecard import (
    CEOScorecardStatus,
    RecommendationType,
    RecommendationPriority
)


# CEO Behavior Score schemas
class CEOBehaviorScoreBase(BaseModel):
    # Decisiveness
    decision_speed: Optional[int] = None
    decision_quality: Optional[int] = None
    loss_cutting: Optional[int] = None
    ambiguity_handling: Optional[int] = None
    # Reliability
    predictability: Optional[int] = None
    commitment_delivery: Optional[int] = None
    process_discipline: Optional[int] = None
    time_management: Optional[int] = None
    # Bold Adaptation
    pivot_capacity: Optional[int] = None
    inflection_recognition: Optional[int] = None
    experimentation_velocity: Optional[int] = None
    learning_agility: Optional[int] = None
    # Engaging for Impact
    stakeholder_influence: Optional[int] = None
    cross_functional_alignment: Optional[int] = None
    vision_communication: Optional[int] = None
    talent_magnetism: Optional[int] = None
    notes: Optional[str] = None


class CEOBehaviorScoreCreate(CEOBehaviorScoreBase):
    pass


class CEOBehaviorScore(CEOBehaviorScoreBase):
    id: UUID4
    ceo_scorecard_id: UUID4
    decisiveness_score: Optional[float]
    reliability_score: Optional[float]
    bold_adaptation_score: Optional[float]
    engaging_impact_score: Optional[float]
    overall_behavior_score: Optional[float]
    weakest_behavior: Optional[str]
    strongest_behavior: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# CEO Power Score schemas
class CEOPowerScoreBase(BaseModel):
    # Priorities (P)
    clarity_score: Optional[int] = None
    focus_score: Optional[int] = None
    alignment_score: Optional[int] = None
    resource_consistency_score: Optional[int] = None
    # Who (W)
    bench_strength_score: Optional[int] = None
    a_player_ratio_score: Optional[int] = None
    team_gaps_score: Optional[int] = None
    delegation_efficiency_score: Optional[int] = None
    # Relationships (R)
    board_alignment_score: Optional[int] = None
    cross_team_collaboration_score: Optional[int] = None
    market_trust_score: Optional[int] = None
    culture_health_score: Optional[int] = None
    notes: Optional[str] = None


class CEOPowerScoreCreate(CEOPowerScoreBase):
    pass


class CEOPowerScore(CEOPowerScoreBase):
    id: UUID4
    ceo_scorecard_id: UUID4
    priorities_score: Optional[float]
    who_score: Optional[float]
    relationships_score: Optional[float]
    total_power_score: Optional[float]
    weakest_dimension: Optional[str]
    weakest_sub_component: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# CEO Operating Metrics schemas
class CEOOperatingMetricsBase(BaseModel):
    quarterly_goal_achievement: Optional[int] = None
    revenue_target_performance: Optional[int] = None
    cash_runway_discipline: Optional[int] = None
    strategy_execution_score: Optional[int] = None
    people_leadership_score: Optional[int] = None
    org_engagement_score: Optional[int] = None
    customer_impact_score: Optional[int] = None
    revenue_actual: Optional[float] = None
    revenue_target: Optional[float] = None
    cash_runway_months: Optional[float] = None
    team_size: Optional[int] = None
    customer_nps: Optional[int] = None
    notes: Optional[str] = None


class CEOOperatingMetricsCreate(CEOOperatingMetricsBase):
    pass


class CEOOperatingMetrics(CEOOperatingMetricsBase):
    id: UUID4
    ceo_scorecard_id: UUID4
    overall_operating_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


# CEO Recommendation schemas
class CEORecommendationBase(BaseModel):
    recommendation_type: RecommendationType
    priority: RecommendationPriority
    title: str
    description: str
    action_items: List[Dict] = []
    expected_impact: Optional[str] = None


class CEORecommendationCreate(CEORecommendationBase):
    pass


class CEORecommendation(CEORecommendationBase):
    id: UUID4
    ceo_scorecard_id: UUID4
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# CEO Scorecard schemas
class CEOScorecardBase(BaseModel):
    period: str
    status: CEOScorecardStatus = CEOScorecardStatus.DRAFT


class CEOScorecardCreate(CEOScorecardBase):
    ceo_id: UUID4
    organization_id: UUID4
    behavior_scores: Optional[CEOBehaviorScoreCreate] = None
    power_scores: Optional[CEOPowerScoreCreate] = None
    operating_metrics: Optional[CEOOperatingMetricsCreate] = None


class CEOScorecardUpdate(BaseModel):
    period: Optional[str] = None
    status: Optional[CEOScorecardStatus] = None


class CEOScorecard(CEOScorecardBase):
    id: UUID4
    ceo_id: UUID4
    organization_id: UUID4
    ceo_excellence_index: Optional[float]
    created_at: datetime
    updated_at: datetime
    finalized_at: Optional[datetime]

    class Config:
        from_attributes = True


class CEOScorecardWithDetails(CEOScorecard):
    """Full CEO Scorecard with all components"""
    behavior_scores: Optional[List[CEOBehaviorScore]] = []
    power_scores: Optional[List[CEOPowerScore]] = []
    operating_metrics: Optional[List[CEOOperatingMetrics]] = []
    recommendations: Optional[List[CEORecommendation]] = []

    class Config:
        from_attributes = True


# CEO Excellence Index response
class CEOExcellenceIndex(BaseModel):
    ceo_scorecard_id: UUID4
    excellence_index: float
    behavior_score: float
    power_score: float
    operating_score: float
    weakest_area: str
    top_recommendations: List[CEORecommendation]

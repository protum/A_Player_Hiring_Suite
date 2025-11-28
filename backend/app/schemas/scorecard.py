"""
Scorecard schemas (A-Method)
"""
from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict
from datetime import datetime
from app.models.scorecard import ScorecardStatus


# Outcome schemas
class ScorecardOutcomeBase(BaseModel):
    description: str
    metric: str
    target_value: str
    timeframe: str
    priority: int = 1


class ScorecardOutcomeCreate(ScorecardOutcomeBase):
    pass


class ScorecardOutcome(ScorecardOutcomeBase):
    id: UUID4
    scorecard_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True


# Competency schemas
class ScorecardCompetencyBase(BaseModel):
    competency_name: str
    description: str
    behavioral_anchors: Dict = {}
    weight: float = 1.0


class ScorecardCompetencyCreate(ScorecardCompetencyBase):
    pass


class ScorecardCompetency(ScorecardCompetencyBase):
    id: UUID4
    scorecard_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True


# Scorecard schemas
class ScorecardBase(BaseModel):
    role_title: str
    role_mission: str
    status: ScorecardStatus = ScorecardStatus.DRAFT


class ScorecardCreate(ScorecardBase):
    organization_id: UUID4
    outcomes: Optional[List[ScorecardOutcomeCreate]] = []
    competencies: Optional[List[ScorecardCompetencyCreate]] = []


class ScorecardUpdate(BaseModel):
    role_title: Optional[str] = None
    role_mission: Optional[str] = None
    status: Optional[ScorecardStatus] = None


class Scorecard(ScorecardBase):
    id: UUID4
    organization_id: UUID4
    created_by_id: Optional[UUID4]
    created_at: datetime
    updated_at: datetime
    outcomes: List[ScorecardOutcome] = []
    competencies: List[ScorecardCompetency] = []

    class Config:
        from_attributes = True


class ScorecardWithDetails(Scorecard):
    """Extended scorecard with full details"""
    pass

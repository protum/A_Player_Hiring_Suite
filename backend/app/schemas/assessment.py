"""Assessment schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# CEO Assessment Schemas
class BehaviorRatingCreate(BaseModel):
    """Schema for creating a behavior rating."""

    behavior: str = Field(..., pattern="^(decisiveness|reliability|adaptation|engagement)$")
    score: int = Field(..., ge=1, le=5)
    evidence: Optional[str] = None
    development_notes: Optional[str] = None


class BehaviorRatingResponse(BehaviorRatingCreate):
    """Schema for behavior rating response."""

    id: str
    assessment_id: str

    class Config:
        from_attributes = True


class CEOAssessmentCreate(BaseModel):
    """Schema for creating a CEO assessment."""

    subject_id: str
    assessment_date: datetime
    assessment_type: str = Field(..., pattern="^(self|observer|360)$")
    assessor_name: Optional[str] = None
    notes: Optional[str] = None
    behavior_ratings: List[BehaviorRatingCreate]


class CEOAssessmentResponse(BaseModel):
    """Schema for CEO assessment response."""

    id: str
    subject_id: str
    assessment_date: datetime
    assessment_type: str
    assessor_name: Optional[str]
    overall_score: Optional[float]
    notes: Optional[str]
    created_at: datetime
    behavior_ratings: List[BehaviorRatingResponse]

    class Config:
        from_attributes = True


# Power Score Schemas
class PowerScoreResponseCreate(BaseModel):
    """Schema for creating a power score question response."""

    dimension: str = Field(..., pattern="^(results|relationships|role_model)$")
    question_id: str
    question_text: str
    response_value: Optional[int] = Field(None, ge=1, le=5)
    response_text: Optional[str] = None


class PowerScoreResponseItem(PowerScoreResponseCreate):
    """Schema for power score response item."""

    id: str
    assessment_id: str

    class Config:
        from_attributes = True


class DevelopmentPlanCreate(BaseModel):
    """Schema for creating a development plan."""

    dimension: str = Field(..., pattern="^(results|relationships|role_model)$")
    goal: str = Field(..., min_length=1)
    action_steps: Optional[str] = None
    target_date: Optional[date] = None
    status: Optional[str] = "active"


class DevelopmentPlanResponse(DevelopmentPlanCreate):
    """Schema for development plan response."""

    id: str
    assessment_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PowerScoreAssessmentCreate(BaseModel):
    """Schema for creating a power score assessment."""

    subject_id: str
    assessment_date: datetime
    notes: Optional[str] = None
    responses: List[PowerScoreResponseCreate]
    development_plans: List[DevelopmentPlanCreate] = Field(default_factory=list)


class PowerScoreAssessmentResponse(BaseModel):
    """Schema for power score assessment response."""

    id: str
    subject_id: str
    assessment_date: datetime
    results_score: float
    relationships_score: float
    role_model_score: float
    overall_power_score: float
    notes: Optional[str]
    created_at: datetime
    responses: List[PowerScoreResponseItem]
    development_plans: List[DevelopmentPlanResponse]

    class Config:
        from_attributes = True

"""Scorecard schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IndicatorCreate(BaseModel):
    """Schema for creating a competency indicator."""

    indicator: str = Field(..., min_length=1)


class IndicatorResponse(IndicatorCreate):
    """Schema for indicator response."""

    id: str

    class Config:
        from_attributes = True


class OutcomeCreate(BaseModel):
    """Schema for creating an outcome."""

    description: str = Field(..., min_length=1)
    metric: Optional[str] = None
    timeframe: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=10)


class OutcomeResponse(OutcomeCreate):
    """Schema for outcome response."""

    id: str
    scorecard_id: str

    class Config:
        from_attributes = True


class CompetencyCreate(BaseModel):
    """Schema for creating a competency."""

    name: str = Field(..., min_length=1, max_length=200)
    definition: Optional[str] = None
    indicators: List[IndicatorCreate] = Field(default_factory=list)


class CompetencyResponse(BaseModel):
    """Schema for competency response."""

    id: str
    scorecard_id: str
    name: str
    definition: Optional[str]
    indicators: List[IndicatorResponse]

    class Config:
        from_attributes = True


class ScorecardBase(BaseModel):
    """Base scorecard schema."""

    role_title: str = Field(..., min_length=1, max_length=200)
    mission: str = Field(..., min_length=1)
    department: Optional[str] = None
    created_by: Optional[str] = None


class ScorecardCreate(ScorecardBase):
    """Schema for creating a scorecard."""

    outcomes: List[OutcomeCreate] = Field(default_factory=list)
    competencies: List[CompetencyCreate] = Field(default_factory=list)


class ScorecardUpdate(BaseModel):
    """Schema for updating a scorecard."""

    role_title: Optional[str] = Field(None, min_length=1, max_length=200)
    mission: Optional[str] = Field(None, min_length=1)
    department: Optional[str] = None
    created_by: Optional[str] = None


class ScorecardResponse(ScorecardBase):
    """Schema for scorecard response."""

    id: str
    created_at: datetime
    updated_at: datetime
    outcomes: List[OutcomeResponse]
    competencies: List[CompetencyResponse]

    class Config:
        from_attributes = True

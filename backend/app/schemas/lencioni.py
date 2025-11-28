"""Pydantic schemas for Ideal Team Player and Core Values assessments."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Ideal Team Player Schemas
class VirtueRatingCreate(BaseModel):
    """Schema for creating a virtue rating."""

    virtue: str = Field(..., pattern="^(humble|hungry|smart)$")
    question_id: str
    question_text: str
    response_value: int = Field(..., ge=1, le=5)
    evidence: Optional[str] = None


class VirtueRatingResponse(VirtueRatingCreate):
    """Schema for virtue rating response."""

    id: str
    assessment_id: str

    class Config:
        from_attributes = True


class IdealTeamPlayerAssessmentCreate(BaseModel):
    """Schema for creating an Ideal Team Player assessment."""

    subject_id: str
    assessment_date: datetime
    assessment_type: str = Field(..., pattern="^(self|observer|interview)$")
    assessor_name: Optional[str] = None
    notes: Optional[str] = None
    virtue_ratings: List[VirtueRatingCreate]


class IdealTeamPlayerAssessmentResponse(BaseModel):
    """Schema for Ideal Team Player assessment response."""

    id: str
    subject_id: str
    assessment_date: datetime
    assessment_type: str
    assessor_name: Optional[str]
    humble_score: float
    hungry_score: float
    smart_score: float
    overall_score: float
    category: Optional[str]
    notes: Optional[str]
    created_at: datetime
    virtue_ratings: List[VirtueRatingResponse]

    class Config:
        from_attributes = True


# Core Values Schemas
class CoreValueRatingCreate(BaseModel):
    """Schema for creating a core value rating."""

    value: str = Field(
        ...,
        pattern="^(personal_growth|harmonious_relationships|problem_solving|positive_impact|financial_stewardship)$"
    )
    question_id: str
    question_text: str
    response_value: int = Field(..., ge=1, le=5)
    evidence: Optional[str] = None


class CoreValueRatingResponse(CoreValueRatingCreate):
    """Schema for core value rating response."""

    id: str
    assessment_id: str

    class Config:
        from_attributes = True


class CoreValuesAssessmentCreate(BaseModel):
    """Schema for creating a Core Values assessment."""

    subject_id: str
    assessment_date: datetime
    assessment_type: str = Field(..., pattern="^(interview|behavioral|reference)$")
    assessor_name: Optional[str] = None
    notes: Optional[str] = None
    value_ratings: List[CoreValueRatingCreate]


class CoreValuesAssessmentResponse(BaseModel):
    """Schema for Core Values assessment response."""

    id: str
    subject_id: str
    assessment_date: datetime
    assessment_type: str
    assessor_name: Optional[str]
    personal_growth_score: float
    harmonious_relationships_score: float
    problem_solving_score: float
    positive_impact_score: float
    financial_stewardship_score: float
    overall_alignment_score: float
    alignment_level: Optional[str]
    notes: Optional[str]
    created_at: datetime
    value_ratings: List[CoreValueRatingResponse]

    class Config:
        from_attributes = True

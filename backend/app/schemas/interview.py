"""Interview schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class InterviewQuestionCreate(BaseModel):
    """Schema for creating an interview question."""

    question_type: str
    question_text: str
    response: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class InterviewQuestionResponse(InterviewQuestionCreate):
    """Schema for question response."""

    id: str
    job_history_id: str

    class Config:
        from_attributes = True


class JobHistoryCreate(BaseModel):
    """Schema for creating job history."""

    company: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    sequence_order: Optional[int] = None
    responsibilities: Optional[str] = None
    questions: List[InterviewQuestionCreate] = Field(default_factory=list)


class JobHistoryResponse(BaseModel):
    """Schema for job history response."""

    id: str
    interview_id: str
    company: str
    title: str
    start_date: Optional[date]
    end_date: Optional[date]
    sequence_order: Optional[int]
    responsibilities: Optional[str]
    questions: List[InterviewQuestionResponse]

    class Config:
        from_attributes = True


class RedFlagCreate(BaseModel):
    """Schema for creating a red flag."""

    flag_type: str
    description: str
    severity: Optional[str] = None
    job_history_id: Optional[str] = None


class RedFlagResponse(RedFlagCreate):
    """Schema for red flag response."""

    id: str
    interview_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewBase(BaseModel):
    """Base interview schema."""

    candidate_id: str
    scorecard_id: Optional[str] = None
    interview_date: Optional[datetime] = None
    interviewer_name: Optional[str] = None
    status: Optional[str] = "scheduled"
    overall_rating: Optional[str] = None
    hire_recommendation: Optional[bool] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    """Schema for creating an interview."""

    job_history: List[JobHistoryCreate] = Field(default_factory=list)


class InterviewUpdate(BaseModel):
    """Schema for updating an interview."""

    scorecard_id: Optional[str] = None
    interview_date: Optional[datetime] = None
    interviewer_name: Optional[str] = None
    status: Optional[str] = None
    overall_rating: Optional[str] = None
    hire_recommendation: Optional[bool] = None
    notes: Optional[str] = None


class InterviewResponse(InterviewBase):
    """Schema for interview response."""

    id: str
    created_at: datetime
    updated_at: datetime
    job_history: List[JobHistoryResponse]
    red_flags: List[RedFlagResponse]

    class Config:
        from_attributes = True

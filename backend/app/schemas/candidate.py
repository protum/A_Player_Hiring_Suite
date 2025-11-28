"""Candidate schemas."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CandidateBase(BaseModel):
    """Base candidate schema."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    current_title: Optional[str] = None
    linkedin_url: Optional[str] = None


class CandidateCreate(CandidateBase):
    """Schema for creating a candidate."""

    pass


class CandidateUpdate(BaseModel):
    """Schema for updating a candidate."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    current_title: Optional[str] = None
    linkedin_url: Optional[str] = None


class CandidateResponse(CandidateBase):
    """Schema for candidate response."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

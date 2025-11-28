"""
Interview endpoints (Topgrading)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.interview import Interview, InterviewCareerBlock, RedFlag

router = APIRouter()


class InterviewCreate(BaseModel):
    candidate_name: str
    candidate_email: str | None = None
    scorecard_id: UUID | None = None


class InterviewSchema(BaseModel):
    id: UUID
    candidate_name: str
    candidate_email: str | None
    status: str
    overall_rating: float | None
    cqi_score: int | None
    recommendation: str | None

    class Config:
        from_attributes = True


@router.post("/", response_model=InterviewSchema, status_code=status.HTTP_201_CREATED)
async def create_interview(
    interview_data: InterviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new Topgrading interview

    Initiates a chronological in-depth structured interview
    """
    new_interview = Interview(
        candidate_name=interview_data.candidate_name,
        candidate_email=interview_data.candidate_email,
        interviewer_id=current_user.id,
        scorecard_id=interview_data.scorecard_id
    )
    db.add(new_interview)
    await db.commit()
    await db.refresh(new_interview)
    return new_interview


@router.get("/", response_model=List[InterviewSchema])
async def list_interviews(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all interviews"""
    result = await db.execute(
        select(Interview)
        .offset(skip)
        .limit(limit)
        .order_by(Interview.created_at.desc())
    )
    interviews = result.scalars().all()
    return interviews


@router.get("/{interview_id}", response_model=InterviewSchema)
async def get_interview(
    interview_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific interview"""
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    return interview


@router.get("/{interview_id}/red-flags")
async def get_red_flags(
    interview_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all red flags for an interview"""
    result = await db.execute(
        select(RedFlag).where(RedFlag.interview_id == interview_id)
    )
    red_flags = result.scalars().all()
    return red_flags

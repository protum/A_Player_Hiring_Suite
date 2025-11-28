"""
Leadership Assessment endpoints (CEO Next Door 4 Behaviors)
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
from app.models.leadership import LeadershipAssessment, BehaviorRating

router = APIRouter()


class AssessmentCreate(BaseModel):
    subject_id: UUID
    assessment_period: str


class AssessmentSchema(BaseModel):
    id: UUID
    subject_id: UUID
    assessment_period: str
    status: str
    decisiveness_score: float | None
    reliability_score: float | None
    bold_adaptation_score: float | None
    engaging_impact_score: float | None
    overall_score: float | None

    class Config:
        from_attributes = True


@router.post("/assessments", response_model=AssessmentSchema, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment_data: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new Leadership Assessment

    Initiates a 360-degree assessment of the 4 CEO behaviors:
    - Decisiveness
    - Reliability
    - Bold Adaptation
    - Engaging for Impact
    """
    new_assessment = LeadershipAssessment(
        subject_id=assessment_data.subject_id,
        assessment_period=assessment_data.assessment_period
    )
    db.add(new_assessment)
    await db.commit()
    await db.refresh(new_assessment)
    return new_assessment


@router.get("/assessments", response_model=List[AssessmentSchema])
async def list_assessments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all leadership assessments"""
    result = await db.execute(
        select(LeadershipAssessment)
        .offset(skip)
        .limit(limit)
        .order_by(LeadershipAssessment.created_at.desc())
    )
    assessments = result.scalars().all()
    return assessments


@router.get("/assessments/{assessment_id}", response_model=AssessmentSchema)
async def get_assessment(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific leadership assessment"""
    result = await db.execute(
        select(LeadershipAssessment).where(LeadershipAssessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    return assessment

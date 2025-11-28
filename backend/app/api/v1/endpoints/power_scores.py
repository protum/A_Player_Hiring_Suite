"""
Power Score endpoints (P × W × R formula)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.power_score import PowerScore, PriorityAssessment, WhoAssessment, RelationshipAssessment

router = APIRouter()


class PowerScoreCreate(BaseModel):
    executive_id: UUID
    assessment_date: date | None = None


class PowerScoreSchema(BaseModel):
    id: UUID
    executive_id: UUID
    assessment_date: date
    priorities_score: float | None
    who_score: float | None
    relationships_score: float | None
    total_power_score: float | None
    weakest_dimension: str | None

    class Config:
        from_attributes = True


@router.post("/", response_model=PowerScoreSchema, status_code=status.HTTP_201_CREATED)
async def create_power_score(
    power_score_data: PowerScoreCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new Power Score assessment

    Assesses executive effectiveness using the formula:
    Power Score = Priorities (P) × Who (W) × Relationships (R)
    """
    new_power_score = PowerScore(
        executive_id=power_score_data.executive_id,
        assessment_date=power_score_data.assessment_date or date.today()
    )
    db.add(new_power_score)
    await db.commit()
    await db.refresh(new_power_score)
    return new_power_score


@router.get("/", response_model=List[PowerScoreSchema])
async def list_power_scores(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all power scores"""
    result = await db.execute(
        select(PowerScore)
        .offset(skip)
        .limit(limit)
        .order_by(PowerScore.assessment_date.desc())
    )
    power_scores = result.scalars().all()
    return power_scores


@router.get("/{power_score_id}", response_model=PowerScoreSchema)
async def get_power_score(
    power_score_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific power score"""
    result = await db.execute(
        select(PowerScore).where(PowerScore.id == power_score_id)
    )
    power_score = result.scalar_one_or_none()

    if not power_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Power Score not found"
        )

    return power_score


@router.get("/{power_score_id}/weakest-link")
async def get_weakest_link(
    power_score_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Identify the weakest link in Power Score

    Returns the dimension with the lowest score and recommendations
    """
    result = await db.execute(
        select(PowerScore).where(PowerScore.id == power_score_id)
    )
    power_score = result.scalar_one_or_none()

    if not power_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Power Score not found"
        )

    return {
        "power_score_id": power_score.id,
        "weakest_dimension": power_score.weakest_dimension,
        "priorities_score": power_score.priorities_score,
        "who_score": power_score.who_score,
        "relationships_score": power_score.relationships_score,
        "total_power_score": power_score.total_power_score
    }

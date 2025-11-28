"""
Scorecard endpoints (A-Method)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.scorecard import Scorecard, ScorecardOutcome, ScorecardCompetency
from app.schemas.scorecard import (
    ScorecardCreate,
    ScorecardUpdate,
    Scorecard as ScorecardSchema,
    ScorecardWithDetails,
    ScorecardOutcomeCreate,
    ScorecardCompetencyCreate
)

router = APIRouter()


@router.post("/", response_model=ScorecardSchema, status_code=status.HTTP_201_CREATED)
async def create_scorecard(
    scorecard_data: ScorecardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new A-Method Scorecard

    Creates a role scorecard with:
    - Role mission
    - Measurable outcomes (3-5)
    - Key competencies (5-8)
    """
    # Create scorecard
    new_scorecard = Scorecard(
        organization_id=scorecard_data.organization_id,
        created_by_id=current_user.id,
        role_title=scorecard_data.role_title,
        role_mission=scorecard_data.role_mission,
        status=scorecard_data.status
    )
    db.add(new_scorecard)
    await db.flush()

    # Add outcomes
    for outcome_data in scorecard_data.outcomes:
        outcome = ScorecardOutcome(
            scorecard_id=new_scorecard.id,
            **outcome_data.dict()
        )
        db.add(outcome)

    # Add competencies
    for competency_data in scorecard_data.competencies:
        competency = ScorecardCompetency(
            scorecard_id=new_scorecard.id,
            **competency_data.dict()
        )
        db.add(competency)

    await db.commit()
    await db.refresh(new_scorecard)

    return new_scorecard


@router.get("/", response_model=List[ScorecardSchema])
async def list_scorecards(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all scorecards"""
    result = await db.execute(
        select(Scorecard)
        .offset(skip)
        .limit(limit)
        .order_by(Scorecard.created_at.desc())
    )
    scorecards = result.scalars().all()
    return scorecards


@router.get("/{scorecard_id}", response_model=ScorecardWithDetails)
async def get_scorecard(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific scorecard with full details"""
    result = await db.execute(
        select(Scorecard).where(Scorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    await db.refresh(scorecard, ["outcomes", "competencies"])
    return scorecard


@router.put("/{scorecard_id}", response_model=ScorecardSchema)
async def update_scorecard(
    scorecard_id: UUID,
    scorecard_data: ScorecardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a scorecard"""
    result = await db.execute(
        select(Scorecard).where(Scorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    for field, value in scorecard_data.dict(exclude_unset=True).items():
        setattr(scorecard, field, value)

    await db.commit()
    await db.refresh(scorecard)
    return scorecard


@router.delete("/{scorecard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scorecard(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a scorecard"""
    result = await db.execute(
        select(Scorecard).where(Scorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    await db.delete(scorecard)
    await db.commit()
    return None


@router.post("/{scorecard_id}/outcomes", status_code=status.HTTP_201_CREATED)
async def add_outcome(
    scorecard_id: UUID,
    outcome_data: ScorecardOutcomeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add an outcome to a scorecard"""
    outcome = ScorecardOutcome(
        scorecard_id=scorecard_id,
        **outcome_data.dict()
    )
    db.add(outcome)
    await db.commit()
    await db.refresh(outcome)
    return outcome


@router.post("/{scorecard_id}/competencies", status_code=status.HTTP_201_CREATED)
async def add_competency(
    scorecard_id: UUID,
    competency_data: ScorecardCompetencyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a competency to a scorecard"""
    competency = ScorecardCompetency(
        scorecard_id=scorecard_id,
        **competency_data.dict()
    )
    db.add(competency)
    await db.commit()
    await db.refresh(competency)
    return competency

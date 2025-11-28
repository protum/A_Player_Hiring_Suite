"""Scorecard API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from ..models.base import get_db
from ..models.scorecard import Scorecard, ScorecardOutcome, ScorecardCompetency, CompetencyIndicator
from ..schemas.scorecard import ScorecardCreate, ScorecardUpdate, ScorecardResponse
from ..services.pdf_service import generate_scorecard_pdf

router = APIRouter()


@router.get("/", response_model=List[ScorecardResponse])
def list_scorecards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all scorecards with pagination."""
    scorecards = db.query(Scorecard).offset(skip).limit(limit).all()
    return scorecards


@router.post("/", response_model=ScorecardResponse, status_code=status.HTTP_201_CREATED)
def create_scorecard(
    scorecard: ScorecardCreate,
    db: Session = Depends(get_db)
):
    """Create a new scorecard with outcomes and competencies."""
    # Create scorecard
    scorecard_data = scorecard.model_dump(exclude={"outcomes", "competencies"})
    db_scorecard = Scorecard(**scorecard_data)
    db.add(db_scorecard)
    db.flush()

    # Create outcomes
    for outcome in scorecard.outcomes:
        db_outcome = ScorecardOutcome(
            scorecard_id=db_scorecard.id,
            **outcome.model_dump()
        )
        db.add(db_outcome)

    # Create competencies with indicators
    for competency in scorecard.competencies:
        competency_data = competency.model_dump(exclude={"indicators"})
        db_competency = ScorecardCompetency(
            scorecard_id=db_scorecard.id,
            **competency_data
        )
        db.add(db_competency)
        db.flush()

        # Create indicators
        for indicator in competency.indicators:
            db_indicator = CompetencyIndicator(
                competency_id=db_competency.id,
                **indicator.model_dump()
            )
            db.add(db_indicator)

    db.commit()
    db.refresh(db_scorecard)
    return db_scorecard


@router.get("/{scorecard_id}", response_model=ScorecardResponse)
def get_scorecard(
    scorecard_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific scorecard by ID."""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )
    return scorecard


@router.put("/{scorecard_id}", response_model=ScorecardResponse)
def update_scorecard(
    scorecard_id: str,
    scorecard_update: ScorecardUpdate,
    db: Session = Depends(get_db)
):
    """Update a scorecard."""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    update_data = scorecard_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scorecard, field, value)

    db.commit()
    db.refresh(scorecard)
    return scorecard


@router.delete("/{scorecard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scorecard(
    scorecard_id: str,
    db: Session = Depends(get_db)
):
    """Delete a scorecard."""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    db.delete(scorecard)
    db.commit()
    return None


@router.get("/{scorecard_id}/export/pdf")
def export_scorecard_pdf(
    scorecard_id: str,
    db: Session = Depends(get_db)
):
    """Export scorecard to PDF."""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scorecard not found"
        )

    pdf_bytes = generate_scorecard_pdf(scorecard)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=scorecard_{scorecard.role_title}.pdf"
        }
    )

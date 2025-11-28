"""Assessment API endpoints for CEO Behaviors and Power Score."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from ..models.base import get_db
from ..models.assessment import (
    CEOAssessment,
    CEOBehaviorRating,
    PowerScoreAssessment,
    PowerScoreResponse as PowerScoreResponseModel,
    DevelopmentPlan
)
from ..schemas.assessment import (
    CEOAssessmentCreate,
    CEOAssessmentResponse,
    PowerScoreAssessmentCreate,
    PowerScoreAssessmentResponse
)
from ..services.assessment_service import calculate_ceo_overall_score, calculate_power_scores
from ..services.pdf_service import generate_ceo_assessment_pdf, generate_power_score_pdf

router = APIRouter()


# CEO Assessment endpoints
@router.get("/ceo", response_model=List[CEOAssessmentResponse])
def list_ceo_assessments(
    skip: int = 0,
    limit: int = 100,
    subject_id: str = None,
    db: Session = Depends(get_db)
):
    """List all CEO assessments with pagination."""
    query = db.query(CEOAssessment)
    if subject_id:
        query = query.filter(CEOAssessment.subject_id == subject_id)
    assessments = query.offset(skip).limit(limit).all()
    return assessments


@router.post("/ceo", response_model=CEOAssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_ceo_assessment(
    assessment: CEOAssessmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new CEO assessment with behavior ratings."""
    # Create assessment
    assessment_data = assessment.model_dump(exclude={"behavior_ratings"})
    db_assessment = CEOAssessment(**assessment_data)

    # Calculate overall score
    db_assessment.overall_score = calculate_ceo_overall_score(assessment.behavior_ratings)

    db.add(db_assessment)
    db.flush()

    # Create behavior ratings
    for rating in assessment.behavior_ratings:
        db_rating = CEOBehaviorRating(
            assessment_id=db_assessment.id,
            **rating.model_dump()
        )
        db.add(db_rating)

    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get("/ceo/{assessment_id}", response_model=CEOAssessmentResponse)
def get_ceo_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific CEO assessment by ID."""
    assessment = db.query(CEOAssessment).filter(CEOAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return assessment


@router.delete("/ceo/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ceo_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Delete a CEO assessment."""
    assessment = db.query(CEOAssessment).filter(CEOAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()
    return None


@router.get("/ceo/{assessment_id}/export/pdf")
def export_ceo_assessment_pdf(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Export CEO assessment to PDF."""
    assessment = db.query(CEOAssessment).filter(CEOAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    pdf_bytes = generate_ceo_assessment_pdf(assessment, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ceo_assessment_{assessment_id}.pdf"
        }
    )


# Power Score endpoints
@router.get("/power-score", response_model=List[PowerScoreAssessmentResponse])
def list_power_score_assessments(
    skip: int = 0,
    limit: int = 100,
    subject_id: str = None,
    db: Session = Depends(get_db)
):
    """List all Power Score assessments with pagination."""
    query = db.query(PowerScoreAssessment)
    if subject_id:
        query = query.filter(PowerScoreAssessment.subject_id == subject_id)
    assessments = query.offset(skip).limit(limit).all()
    return assessments


@router.post("/power-score", response_model=PowerScoreAssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_power_score_assessment(
    assessment: PowerScoreAssessmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new Power Score assessment with responses."""
    # Calculate scores from responses
    scores = calculate_power_scores(assessment.responses)

    # Create assessment
    assessment_data = assessment.model_dump(exclude={"responses", "development_plans"})
    db_assessment = PowerScoreAssessment(
        **assessment_data,
        results_score=scores["results"],
        relationships_score=scores["relationships"],
        role_model_score=scores["role_model"],
        overall_power_score=scores["overall"]
    )

    db.add(db_assessment)
    db.flush()

    # Create responses
    for response in assessment.responses:
        db_response = PowerScoreResponseModel(
            assessment_id=db_assessment.id,
            **response.model_dump()
        )
        db.add(db_response)

    # Create development plans
    for plan in assessment.development_plans:
        db_plan = DevelopmentPlan(
            assessment_id=db_assessment.id,
            **plan.model_dump()
        )
        db.add(db_plan)

    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get("/power-score/{assessment_id}", response_model=PowerScoreAssessmentResponse)
def get_power_score_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific Power Score assessment by ID."""
    assessment = db.query(PowerScoreAssessment).filter(
        PowerScoreAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return assessment


@router.get("/power-score/{assessment_id}/trends")
def get_power_score_trends(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Get historical trends for a subject based on assessment."""
    assessment = db.query(PowerScoreAssessment).filter(
        PowerScoreAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    # Get all assessments for this subject, ordered by date
    all_assessments = db.query(PowerScoreAssessment).filter(
        PowerScoreAssessment.subject_id == assessment.subject_id
    ).order_by(PowerScoreAssessment.assessment_date).all()

    trends = [
        {
            "date": a.assessment_date,
            "results": a.results_score,
            "relationships": a.relationships_score,
            "role_model": a.role_model_score,
            "overall": a.overall_power_score
        }
        for a in all_assessments
    ]

    return {"trends": trends}


@router.delete("/power-score/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_power_score_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Delete a Power Score assessment."""
    assessment = db.query(PowerScoreAssessment).filter(
        PowerScoreAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()
    return None


@router.get("/power-score/{assessment_id}/export/pdf")
def export_power_score_pdf(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Export Power Score assessment to PDF."""
    assessment = db.query(PowerScoreAssessment).filter(
        PowerScoreAssessment.id == assessment_id
    ).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    pdf_bytes = generate_power_score_pdf(assessment, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=power_score_{assessment_id}.pdf"
        }
    )

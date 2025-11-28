"""API endpoints for Ideal Team Player and Core Values assessments."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from ..models.base import get_db
from ..models.lencioni import (
    IdealTeamPlayerAssessment,
    IdealTeamPlayerVirtueRating,
    CoreValuesAssessment,
    CoreValueRating,
)
from ..schemas.lencioni import (
    IdealTeamPlayerAssessmentCreate,
    IdealTeamPlayerAssessmentResponse,
    CoreValuesAssessmentCreate,
    CoreValuesAssessmentResponse,
)
from ..services.lencioni_service import (
    IDEAL_TEAM_PLAYER_QUESTIONS,
    CORE_VALUES_QUESTIONS,
    calculate_ideal_team_player_scores,
    determine_ideal_team_player_category,
    get_ideal_team_player_insights,
    calculate_core_values_scores,
    determine_core_values_alignment,
    get_core_values_insights,
)
from ..services.pdf_service import (
    generate_ideal_team_player_pdf,
    generate_core_values_pdf,
)

router = APIRouter()


# Ideal Team Player endpoints
@router.get("/ideal-team-player/questions")
def get_ideal_team_player_questions():
    """Get the standard Ideal Team Player assessment questions."""
    return {"questions": IDEAL_TEAM_PLAYER_QUESTIONS}


@router.get("/ideal-team-player", response_model=List[IdealTeamPlayerAssessmentResponse])
def list_ideal_team_player_assessments(
    skip: int = 0,
    limit: int = 100,
    subject_id: str = None,
    db: Session = Depends(get_db),
):
    """List all Ideal Team Player assessments."""
    query = db.query(IdealTeamPlayerAssessment)
    if subject_id:
        query = query.filter(IdealTeamPlayerAssessment.subject_id == subject_id)
    assessments = query.offset(skip).limit(limit).all()
    return assessments


@router.post(
    "/ideal-team-player",
    response_model=IdealTeamPlayerAssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ideal_team_player_assessment(
    assessment: IdealTeamPlayerAssessmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new Ideal Team Player assessment."""
    # Calculate scores
    scores = calculate_ideal_team_player_scores(assessment.virtue_ratings)

    # Determine category
    category = determine_ideal_team_player_category(
        scores["humble_score"], scores["hungry_score"], scores["smart_score"]
    )

    # Create assessment
    assessment_data = assessment.model_dump(exclude={"virtue_ratings"})
    db_assessment = IdealTeamPlayerAssessment(
        **assessment_data,
        humble_score=scores["humble_score"],
        hungry_score=scores["hungry_score"],
        smart_score=scores["smart_score"],
        overall_score=scores["overall_score"],
        category=category,
    )

    db.add(db_assessment)
    db.flush()

    # Create virtue ratings
    for rating in assessment.virtue_ratings:
        db_rating = IdealTeamPlayerVirtueRating(
            assessment_id=db_assessment.id, **rating.model_dump()
        )
        db.add(db_rating)

    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get(
    "/ideal-team-player/{assessment_id}",
    response_model=IdealTeamPlayerAssessmentResponse,
)
def get_ideal_team_player_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific Ideal Team Player assessment."""
    assessment = (
        db.query(IdealTeamPlayerAssessment)
        .filter(IdealTeamPlayerAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )
    return assessment


@router.get("/ideal-team-player/{assessment_id}/insights")
def get_ideal_team_player_assessment_insights(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Get insights and recommendations for an Ideal Team Player assessment."""
    assessment = (
        db.query(IdealTeamPlayerAssessment)
        .filter(IdealTeamPlayerAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    insights = get_ideal_team_player_insights(assessment.category)
    return {
        "assessment_id": assessment_id,
        "category": assessment.category,
        "scores": {
            "humble": assessment.humble_score,
            "hungry": assessment.hungry_score,
            "smart": assessment.smart_score,
            "overall": assessment.overall_score,
        },
        "insights": insights,
    }


@router.delete("/ideal-team-player/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ideal_team_player_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Delete an Ideal Team Player assessment."""
    assessment = (
        db.query(IdealTeamPlayerAssessment)
        .filter(IdealTeamPlayerAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()
    return None


@router.get("/ideal-team-player/{assessment_id}/export/pdf")
def export_ideal_team_player_pdf(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Export Ideal Team Player assessment to PDF."""
    assessment = (
        db.query(IdealTeamPlayerAssessment)
        .filter(IdealTeamPlayerAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    pdf_bytes = generate_ideal_team_player_pdf(assessment, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ideal_team_player_{assessment_id}.pdf"
        },
    )


# Core Values endpoints
@router.get("/core-values/questions")
def get_core_values_questions():
    """Get the standard Core Values assessment questions."""
    return {"questions": CORE_VALUES_QUESTIONS}


@router.get("/core-values", response_model=List[CoreValuesAssessmentResponse])
def list_core_values_assessments(
    skip: int = 0,
    limit: int = 100,
    subject_id: str = None,
    db: Session = Depends(get_db),
):
    """List all Core Values assessments."""
    query = db.query(CoreValuesAssessment)
    if subject_id:
        query = query.filter(CoreValuesAssessment.subject_id == subject_id)
    assessments = query.offset(skip).limit(limit).all()
    return assessments


@router.post(
    "/core-values",
    response_model=CoreValuesAssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_core_values_assessment(
    assessment: CoreValuesAssessmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new Core Values assessment."""
    # Calculate scores
    scores = calculate_core_values_scores(assessment.value_ratings)

    # Determine alignment level
    alignment_level = determine_core_values_alignment(scores["overall_alignment_score"])

    # Create assessment
    assessment_data = assessment.model_dump(exclude={"value_ratings"})
    db_assessment = CoreValuesAssessment(
        **assessment_data,
        personal_growth_score=scores["personal_growth_score"],
        harmonious_relationships_score=scores["harmonious_relationships_score"],
        problem_solving_score=scores["problem_solving_score"],
        positive_impact_score=scores["positive_impact_score"],
        financial_stewardship_score=scores["financial_stewardship_score"],
        overall_alignment_score=scores["overall_alignment_score"],
        alignment_level=alignment_level,
    )

    db.add(db_assessment)
    db.flush()

    # Create value ratings
    for rating in assessment.value_ratings:
        db_rating = CoreValueRating(
            assessment_id=db_assessment.id, **rating.model_dump()
        )
        db.add(db_rating)

    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.get("/core-values/{assessment_id}", response_model=CoreValuesAssessmentResponse)
def get_core_values_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific Core Values assessment."""
    assessment = (
        db.query(CoreValuesAssessment)
        .filter(CoreValuesAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )
    return assessment


@router.get("/core-values/{assessment_id}/insights")
def get_core_values_assessment_insights(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Get insights and recommendations for a Core Values assessment."""
    assessment = (
        db.query(CoreValuesAssessment)
        .filter(CoreValuesAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    scores_dict = {
        "personal_growth_score": assessment.personal_growth_score,
        "harmonious_relationships_score": assessment.harmonious_relationships_score,
        "problem_solving_score": assessment.problem_solving_score,
        "positive_impact_score": assessment.positive_impact_score,
        "financial_stewardship_score": assessment.financial_stewardship_score,
        "overall_alignment_score": assessment.overall_alignment_score,
    }

    insights = get_core_values_insights(assessment.alignment_level, scores_dict)
    return {
        "assessment_id": assessment_id,
        "alignment_level": assessment.alignment_level,
        "scores": scores_dict,
        "insights": insights,
    }


@router.delete("/core-values/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_core_values_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Delete a Core Values assessment."""
    assessment = (
        db.query(CoreValuesAssessment)
        .filter(CoreValuesAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()
    return None


@router.get("/core-values/{assessment_id}/export/pdf")
def export_core_values_pdf(
    assessment_id: str,
    db: Session = Depends(get_db),
):
    """Export Core Values assessment to PDF."""
    assessment = (
        db.query(CoreValuesAssessment)
        .filter(CoreValuesAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
        )

    pdf_bytes = generate_core_values_pdf(assessment, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=core_values_{assessment_id}.pdf"
        },
    )

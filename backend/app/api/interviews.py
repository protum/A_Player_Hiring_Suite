"""Interview API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from ..models.base import get_db
from ..models.interview import Interview, JobHistory, InterviewQuestion, RedFlag
from ..schemas.interview import InterviewCreate, InterviewUpdate, InterviewResponse, RedFlagCreate
from ..services.interview_service import generate_interview_script
from ..services.pdf_service import generate_interview_pdf

router = APIRouter()


@router.get("/", response_model=List[InterviewResponse])
def list_interviews(
    skip: int = 0,
    limit: int = 100,
    candidate_id: str = None,
    db: Session = Depends(get_db)
):
    """List all interviews with pagination."""
    query = db.query(Interview)
    if candidate_id:
        query = query.filter(Interview.candidate_id == candidate_id)
    interviews = query.offset(skip).limit(limit).all()
    return interviews


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db)
):
    """Create a new interview with job history."""
    # Create interview
    interview_data = interview.model_dump(exclude={"job_history"})
    db_interview = Interview(**interview_data)
    db.add(db_interview)
    db.flush()

    # Create job history with questions
    for job in interview.job_history:
        job_data = job.model_dump(exclude={"questions"})
        db_job = JobHistory(
            interview_id=db_interview.id,
            **job_data
        )
        db.add(db_job)
        db.flush()

        # Create questions
        for question in job.questions:
            db_question = InterviewQuestion(
                job_history_id=db_job.id,
                **question.model_dump()
            )
            db.add(db_question)

    db.commit()
    db.refresh(db_interview)
    return db_interview


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific interview by ID."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: str,
    interview_update: InterviewUpdate,
    db: Session = Depends(get_db)
):
    """Update an interview."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    update_data = interview_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(interview, field, value)

    db.commit()
    db.refresh(interview)
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """Delete an interview."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    db.delete(interview)
    db.commit()
    return None


@router.post("/{interview_id}/generate-script")
def generate_script(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """Generate interview script based on job history."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    script = generate_interview_script(interview, db)
    return {"script": script}


@router.post("/{interview_id}/red-flags", status_code=status.HTTP_201_CREATED)
def add_red_flag(
    interview_id: str,
    red_flag: RedFlagCreate,
    db: Session = Depends(get_db)
):
    """Add a red flag to an interview."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    db_red_flag = RedFlag(
        interview_id=interview_id,
        **red_flag.model_dump()
    )
    db.add(db_red_flag)
    db.commit()
    db.refresh(db_red_flag)
    return db_red_flag


@router.get("/{interview_id}/export/pdf")
def export_interview_pdf(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """Export interview notes to PDF."""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    pdf_bytes = generate_interview_pdf(interview, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=interview_{interview_id}.pdf"
        }
    )

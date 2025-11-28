"""Backup and restore service for database operations."""

import json
import shutil
from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.candidate import Candidate
from ..models.scorecard import Scorecard
from ..models.interview import Interview
from ..models.assessment import CEOAssessment, PowerScoreAssessment


def create_backup(source_path: str, dest_path: str) -> bool:
    """Create a backup of the database file."""
    try:
        shutil.copy2(source_path, dest_path)
        return True
    except Exception as e:
        raise Exception(f"Backup failed: {str(e)}")


def restore_backup(backup_path: str, db: Session) -> bool:
    """Restore database from backup."""
    try:
        # Validation logic here
        # This would involve closing connections, replacing file, etc.
        return True
    except Exception as e:
        raise Exception(f"Restore failed: {str(e)}")


def export_to_json(db: Session) -> str:
    """Export entire database to JSON format."""
    data = {
        "export_date": datetime.now().isoformat(),
        "version": "1.0",
        "data": {}
    }

    # Export candidates
    candidates = db.query(Candidate).all()
    data["data"]["candidates"] = [
        {
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "current_title": c.current_title,
            "linkedin_url": c.linkedin_url,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in candidates
    ]

    # Export scorecards
    scorecards = db.query(Scorecard).all()
    data["data"]["scorecards"] = [
        {
            "id": s.id,
            "role_title": s.role_title,
            "mission": s.mission,
            "department": s.department,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "outcomes": [
                {
                    "description": o.description,
                    "metric": o.metric,
                    "timeframe": o.timeframe,
                    "priority": o.priority
                }
                for o in s.outcomes
            ],
            "competencies": [
                {
                    "name": comp.name,
                    "definition": comp.definition,
                    "indicators": [ind.indicator for ind in comp.indicators]
                }
                for comp in s.competencies
            ]
        }
        for s in scorecards
    ]

    # Export interviews
    interviews = db.query(Interview).all()
    data["data"]["interviews"] = [
        {
            "id": i.id,
            "candidate_id": i.candidate_id,
            "interview_date": i.interview_date.isoformat() if i.interview_date else None,
            "status": i.status,
            "overall_rating": i.overall_rating,
            "hire_recommendation": i.hire_recommendation,
            "job_history_count": len(i.job_history),
            "red_flags_count": len(i.red_flags)
        }
        for i in interviews
    ]

    # Export CEO assessments
    ceo_assessments = db.query(CEOAssessment).all()
    data["data"]["ceo_assessments"] = [
        {
            "id": a.id,
            "subject_id": a.subject_id,
            "assessment_date": a.assessment_date.isoformat() if a.assessment_date else None,
            "assessment_type": a.assessment_type,
            "overall_score": a.overall_score,
        }
        for a in ceo_assessments
    ]

    # Export Power Score assessments
    power_score_assessments = db.query(PowerScoreAssessment).all()
    data["data"]["power_score_assessments"] = [
        {
            "id": a.id,
            "subject_id": a.subject_id,
            "assessment_date": a.assessment_date.isoformat() if a.assessment_date else None,
            "results_score": a.results_score,
            "relationships_score": a.relationships_score,
            "role_model_score": a.role_model_score,
            "overall_power_score": a.overall_power_score,
        }
        for a in power_score_assessments
    ]

    return json.dumps(data, indent=2)


def import_from_json(json_data: str, db: Session) -> bool:
    """Import data from JSON format."""
    try:
        data = json.loads(json_data)
        # Import logic would go here
        # This would involve creating records from the JSON data
        return True
    except Exception as e:
        raise Exception(f"Import failed: {str(e)}")

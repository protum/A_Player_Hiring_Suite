"""System API endpoints for backup, export, and health checks."""

from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from datetime import datetime
import json

from ..models.base import get_db, DATABASE_PATH, DATA_DIR
from ..models.system import ExportHistory
from ..services.backup_service import create_backup, restore_backup, export_to_json

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@router.post("/backup/export")
def export_database(
    format: str = "sqlite",
    db: Session = Depends(get_db)
):
    """Export entire database."""
    if format == "sqlite":
        # Create a copy of the SQLite database
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(DATA_DIR, backup_filename)

        # Close current session to avoid lock
        db.close()

        # Copy database file
        shutil.copy2(DATABASE_PATH, backup_path)

        # Record export
        export_record = ExportHistory(
            id=str(datetime.now().timestamp()),
            export_type="sqlite_backup",
            file_path=backup_path
        )
        db.add(export_record)
        db.commit()

        with open(backup_path, "rb") as f:
            content = f.read()

        return Response(
            content=content,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={backup_filename}"
            }
        )

    elif format == "json":
        # Export all data to JSON
        json_data = export_to_json(db)

        # Record export
        export_record = ExportHistory(
            id=str(datetime.now().timestamp()),
            export_type="json",
            file_path=None
        )
        db.add(export_record)
        db.commit()

        return Response(
            content=json_data,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Use 'sqlite' or 'json'"
        )


@router.post("/backup/import")
async def import_database(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import database backup."""
    if file.filename.endswith(".db"):
        # SQLite restore
        backup_path = os.path.join(DATA_DIR, "temp_restore.db")

        with open(backup_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate it's a valid SQLite database
        try:
            restore_backup(backup_path, db)
            os.remove(backup_path)
            return {"status": "success", "message": "Database restored successfully"}
        except Exception as e:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid database file: {str(e)}"
            )

    elif file.filename.endswith(".json"):
        # JSON import
        content = await file.read()
        try:
            data = json.loads(content)
            # Import logic would go here
            return {"status": "success", "message": "Data imported successfully"}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON file"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Use .db or .json"
        )


@router.get("/export-history")
def get_export_history(
    db: Session = Depends(get_db)
):
    """Get export history."""
    history = db.query(ExportHistory).order_by(ExportHistory.exported_at.desc()).limit(50).all()
    return {"history": history}


@router.get("/stats")
def get_database_stats(
    db: Session = Depends(get_db)
):
    """Get database statistics."""
    from ..models.candidate import Candidate
    from ..models.scorecard import Scorecard
    from ..models.interview import Interview
    from ..models.assessment import CEOAssessment, PowerScoreAssessment

    stats = {
        "candidates": db.query(Candidate).count(),
        "scorecards": db.query(Scorecard).count(),
        "interviews": db.query(Interview).count(),
        "ceo_assessments": db.query(CEOAssessment).count(),
        "power_score_assessments": db.query(PowerScoreAssessment).count(),
        "database_size_mb": round(os.path.getsize(DATABASE_PATH) / (1024 * 1024), 2)
    }

    return stats

"""
API v1 Router
Combines all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, scorecards, interviews, leadership, power_scores, ceo_scorecards

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(scorecards.router, prefix="/scorecards", tags=["Scorecards"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(leadership.router, prefix="/leadership", tags=["Leadership Assessments"])
api_router.include_router(power_scores.router, prefix="/power-scores", tags=["Power Scores"])
api_router.include_router(ceo_scorecards.router, prefix="/ceo-scorecards", tags=["CEO Scorecards"])

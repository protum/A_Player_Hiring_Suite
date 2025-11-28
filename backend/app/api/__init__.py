"""API routes for A-Player Hiring Suite."""

from fastapi import APIRouter
from .candidates import router as candidates_router
from .scorecards import router as scorecards_router
from .interviews import router as interviews_router
from .assessments import router as assessments_router
from .lencioni import router as lencioni_router
from .system import router as system_router

api_router = APIRouter(prefix="/api")

api_router.include_router(candidates_router, prefix="/candidates", tags=["candidates"])
api_router.include_router(scorecards_router, prefix="/scorecards", tags=["scorecards"])
api_router.include_router(interviews_router, prefix="/interviews", tags=["interviews"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["assessments"])
api_router.include_router(lencioni_router, prefix="/assessments", tags=["lencioni"])
api_router.include_router(system_router, prefix="/system", tags=["system"])

__all__ = ["api_router"]

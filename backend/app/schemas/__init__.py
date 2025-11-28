"""Pydantic schemas for request/response validation."""

from .candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from .scorecard import (
    ScorecardCreate,
    ScorecardUpdate,
    ScorecardResponse,
    OutcomeCreate,
    CompetencyCreate,
)
from .interview import (
    InterviewCreate,
    InterviewUpdate,
    InterviewResponse,
    JobHistoryCreate,
    InterviewQuestionCreate,
    RedFlagCreate,
)
from .assessment import (
    CEOAssessmentCreate,
    CEOAssessmentResponse,
    BehaviorRatingCreate,
    PowerScoreAssessmentCreate,
    PowerScoreAssessmentResponse,
    DevelopmentPlanCreate,
)

__all__ = [
    "CandidateCreate",
    "CandidateUpdate",
    "CandidateResponse",
    "ScorecardCreate",
    "ScorecardUpdate",
    "ScorecardResponse",
    "OutcomeCreate",
    "CompetencyCreate",
    "InterviewCreate",
    "InterviewUpdate",
    "InterviewResponse",
    "JobHistoryCreate",
    "InterviewQuestionCreate",
    "RedFlagCreate",
    "CEOAssessmentCreate",
    "CEOAssessmentResponse",
    "BehaviorRatingCreate",
    "PowerScoreAssessmentCreate",
    "PowerScoreAssessmentResponse",
    "DevelopmentPlanCreate",
]

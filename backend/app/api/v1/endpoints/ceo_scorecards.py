"""
CEO Scorecard endpoints
Comprehensive executive performance assessment
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user, BoardOrAdmin
from app.models.user import User
from app.models.ceo_scorecard import (
    CEOScorecard,
    CEOBehaviorScore,
    CEOPowerScore,
    CEOOperatingMetrics,
    CEORecommendation,
    CEOScorecardStatus,
    RecommendationType,
    RecommendationPriority
)
from app.schemas.ceo_scorecard import (
    CEOScorecardCreate,
    CEOScorecardUpdate,
    CEOScorecard as CEOScorecardSchema,
    CEOScorecardWithDetails,
    CEOBehaviorScoreCreate,
    CEOPowerScoreCreate,
    CEOOperatingMetricsCreate,
    CEOExcellenceIndex,
    CEORecommendation as CEORecommendationSchema
)

router = APIRouter()


def calculate_ceo_excellence_index(
    behavior_score: CEOBehaviorScore,
    power_score: CEOPowerScore,
    operating_metrics: CEOOperatingMetrics
) -> float:
    """
    Calculate CEO Excellence Index (0-100)
    Weighted combination of all dimensions
    """
    # Weights: Behaviors 30%, Power Score 30%, Operating Metrics 40%
    behavior_component = (behavior_score.overall_behavior_score or 0) * 10 * 0.30
    power_component = (power_score.total_power_score or 0) / 10 * 0.30
    operating_component = (operating_metrics.overall_operating_score or 0) * 0.40

    excellence_index = behavior_component + power_component + operating_component
    return round(excellence_index, 2)


def calculate_behavior_scores(behavior_data: CEOBehaviorScoreCreate) -> dict:
    """Calculate aggregate behavior scores"""
    # Decisiveness
    decisiveness_scores = [
        behavior_data.decision_speed or 0,
        behavior_data.decision_quality or 0,
        behavior_data.loss_cutting or 0,
        behavior_data.ambiguity_handling or 0
    ]
    decisiveness = sum(decisiveness_scores) / len([s for s in decisiveness_scores if s > 0]) if any(decisiveness_scores) else 0

    # Reliability
    reliability_scores = [
        behavior_data.predictability or 0,
        behavior_data.commitment_delivery or 0,
        behavior_data.process_discipline or 0,
        behavior_data.time_management or 0
    ]
    reliability = sum(reliability_scores) / len([s for s in reliability_scores if s > 0]) if any(reliability_scores) else 0

    # Bold Adaptation
    bold_scores = [
        behavior_data.pivot_capacity or 0,
        behavior_data.inflection_recognition or 0,
        behavior_data.experimentation_velocity or 0,
        behavior_data.learning_agility or 0
    ]
    bold_adaptation = sum(bold_scores) / len([s for s in bold_scores if s > 0]) if any(bold_scores) else 0

    # Engaging for Impact
    engaging_scores = [
        behavior_data.stakeholder_influence or 0,
        behavior_data.cross_functional_alignment or 0,
        behavior_data.vision_communication or 0,
        behavior_data.talent_magnetism or 0
    ]
    engaging = sum(engaging_scores) / len([s for s in engaging_scores if s > 0]) if any(engaging_scores) else 0

    # Overall
    behavior_scores_list = [decisiveness, reliability, bold_adaptation, engaging]
    overall = sum(behavior_scores_list) / len([s for s in behavior_scores_list if s > 0]) if any(behavior_scores_list) else 0

    # Find weakest and strongest
    score_map = {
        "decisiveness": decisiveness,
        "reliability": reliability,
        "bold_adaptation": bold_adaptation,
        "engaging_impact": engaging
    }
    weakest = min(score_map, key=score_map.get) if any(score_map.values()) else None
    strongest = max(score_map, key=score_map.get) if any(score_map.values()) else None

    return {
        "decisiveness_score": round(decisiveness, 2),
        "reliability_score": round(reliability, 2),
        "bold_adaptation_score": round(bold_adaptation, 2),
        "engaging_impact_score": round(engaging, 2),
        "overall_behavior_score": round(overall, 2),
        "weakest_behavior": weakest,
        "strongest_behavior": strongest
    }


def calculate_power_scores(power_data: CEOPowerScoreCreate) -> dict:
    """Calculate Power Score (P × W × R)"""
    # Priorities (P)
    p_scores = [
        power_data.clarity_score or 0,
        power_data.focus_score or 0,
        power_data.alignment_score or 0,
        power_data.resource_consistency_score or 0
    ]
    p_avg = sum(p_scores) / len([s for s in p_scores if s > 0]) if any(p_scores) else 0

    # Who (W)
    w_scores = [
        power_data.bench_strength_score or 0,
        power_data.a_player_ratio_score or 0,
        power_data.team_gaps_score or 0,
        power_data.delegation_efficiency_score or 0
    ]
    w_avg = sum(w_scores) / len([s for s in w_scores if s > 0]) if any(w_scores) else 0

    # Relationships (R)
    r_scores = [
        power_data.board_alignment_score or 0,
        power_data.cross_team_collaboration_score or 0,
        power_data.market_trust_score or 0,
        power_data.culture_health_score or 0
    ]
    r_avg = sum(r_scores) / len([s for s in r_scores if s > 0]) if any(r_scores) else 0

    # Total Power Score = P × W × R
    total = p_avg * w_avg * r_avg

    # Find weakest dimension
    dim_map = {"priorities": p_avg, "who": w_avg, "relationships": r_avg}
    weakest_dim = min(dim_map, key=dim_map.get) if any(dim_map.values()) else None

    # Find weakest sub-component
    all_scores = {
        "clarity": power_data.clarity_score or 0,
        "focus": power_data.focus_score or 0,
        "alignment": power_data.alignment_score or 0,
        "resource_consistency": power_data.resource_consistency_score or 0,
        "bench_strength": power_data.bench_strength_score or 0,
        "a_player_ratio": power_data.a_player_ratio_score or 0,
        "team_gaps": power_data.team_gaps_score or 0,
        "delegation_efficiency": power_data.delegation_efficiency_score or 0,
        "board_alignment": power_data.board_alignment_score or 0,
        "cross_team_collaboration": power_data.cross_team_collaboration_score or 0,
        "market_trust": power_data.market_trust_score or 0,
        "culture_health": power_data.culture_health_score or 0,
    }
    weakest_sub = min(all_scores, key=all_scores.get) if any(all_scores.values()) else None

    return {
        "priorities_score": round(p_avg, 2),
        "who_score": round(w_avg, 2),
        "relationships_score": round(r_avg, 2),
        "total_power_score": round(total, 2),
        "weakest_dimension": weakest_dim,
        "weakest_sub_component": weakest_sub
    }


def calculate_operating_score(metrics_data: CEOOperatingMetricsCreate) -> float:
    """Calculate overall operating score"""
    scores = [
        metrics_data.quarterly_goal_achievement or 0,
        metrics_data.revenue_target_performance or 0,
        metrics_data.cash_runway_discipline or 0,
        metrics_data.strategy_execution_score or 0,
        metrics_data.people_leadership_score or 0,
        metrics_data.org_engagement_score or 0,
        metrics_data.customer_impact_score or 0
    ]
    avg = sum(scores) / len([s for s in scores if s > 0]) if any(scores) else 0
    return round(avg, 2)


@router.post("/", response_model=CEOScorecardSchema, status_code=status.HTTP_201_CREATED)
async def create_ceo_scorecard(
    scorecard_data: CEOScorecardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new CEO Scorecard

    Creates a comprehensive executive performance scorecard combining:
    - CEO Next Door 4 Behaviors
    - Power Score (P × W × R)
    - Operating Metrics
    """
    # Create scorecard
    new_scorecard = CEOScorecard(
        ceo_id=scorecard_data.ceo_id,
        organization_id=scorecard_data.organization_id,
        period=scorecard_data.period,
        status=scorecard_data.status
    )
    db.add(new_scorecard)
    await db.flush()

    # Add behavior scores if provided
    if scorecard_data.behavior_scores:
        calc_scores = calculate_behavior_scores(scorecard_data.behavior_scores)
        behavior_score = CEOBehaviorScore(
            ceo_scorecard_id=new_scorecard.id,
            **scorecard_data.behavior_scores.dict(exclude_unset=True),
            **calc_scores
        )
        db.add(behavior_score)

    # Add power scores if provided
    if scorecard_data.power_scores:
        calc_power = calculate_power_scores(scorecard_data.power_scores)
        power_score = CEOPowerScore(
            ceo_scorecard_id=new_scorecard.id,
            **scorecard_data.power_scores.dict(exclude_unset=True),
            **calc_power
        )
        db.add(power_score)

    # Add operating metrics if provided
    if scorecard_data.operating_metrics:
        op_score = calculate_operating_score(scorecard_data.operating_metrics)
        operating_metrics = CEOOperatingMetrics(
            ceo_scorecard_id=new_scorecard.id,
            **scorecard_data.operating_metrics.dict(exclude_unset=True),
            overall_operating_score=op_score
        )
        db.add(operating_metrics)

    await db.commit()
    await db.refresh(new_scorecard)

    return new_scorecard


@router.get("/", response_model=List[CEOScorecardSchema])
async def list_ceo_scorecards(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all CEO Scorecards

    Supports pagination via skip and limit parameters
    """
    result = await db.execute(
        select(CEOScorecard)
        .offset(skip)
        .limit(limit)
        .order_by(CEOScorecard.created_at.desc())
    )
    scorecards = result.scalars().all()
    return scorecards


@router.get("/{scorecard_id}", response_model=CEOScorecardWithDetails)
async def get_ceo_scorecard(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific CEO Scorecard with full details

    Returns the complete scorecard including:
    - Behavior scores
    - Power scores
    - Operating metrics
    - Recommendations
    """
    result = await db.execute(
        select(CEOScorecard).where(CEOScorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CEO Scorecard not found"
        )

    # Load related data
    await db.refresh(scorecard, ["behavior_scores", "power_scores", "operating_metrics", "recommendations"])

    return scorecard


@router.put("/{scorecard_id}", response_model=CEOScorecardSchema)
async def update_ceo_scorecard(
    scorecard_id: UUID,
    scorecard_data: CEOScorecardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a CEO Scorecard
    """
    result = await db.execute(
        select(CEOScorecard).where(CEOScorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CEO Scorecard not found"
        )

    # Update fields
    for field, value in scorecard_data.dict(exclude_unset=True).items():
        setattr(scorecard, field, value)

    await db.commit()
    await db.refresh(scorecard)

    return scorecard


@router.post("/{scorecard_id}/finalize", response_model=CEOScorecardSchema)
async def finalize_ceo_scorecard(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(BoardOrAdmin)
):
    """
    Finalize a CEO Scorecard

    Requires board member or admin role
    Calculates final excellence index and generates recommendations
    """
    result = await db.execute(
        select(CEOScorecard).where(CEOScorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CEO Scorecard not found"
        )

    # Load related data
    await db.refresh(scorecard, ["behavior_scores", "power_scores", "operating_metrics"])

    if not scorecard.behavior_scores or not scorecard.power_scores or not scorecard.operating_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot finalize scorecard: missing behavior scores, power scores, or operating metrics"
        )

    # Calculate excellence index
    behavior_score = scorecard.behavior_scores[0]
    power_score = scorecard.power_scores[0]
    operating_metrics = scorecard.operating_metrics[0]

    excellence_index = calculate_ceo_excellence_index(behavior_score, power_score, operating_metrics)

    # Update scorecard
    scorecard.ceo_excellence_index = excellence_index
    scorecard.status = CEOScorecardStatus.FINALIZED
    from datetime import datetime
    scorecard.finalized_at = datetime.utcnow()

    await db.commit()
    await db.refresh(scorecard)

    return scorecard


@router.get("/{scorecard_id}/excellence-index", response_model=CEOExcellenceIndex)
async def get_excellence_index(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get CEO Excellence Index and analysis

    Returns comprehensive analysis including:
    - Excellence index score
    - Component scores
    - Weakest areas
    - Top recommendations
    """
    result = await db.execute(
        select(CEOScorecard).where(CEOScorecard.id == scorecard_id)
    )
    scorecard = result.scalar_one_or_none()

    if not scorecard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CEO Scorecard not found"
        )

    # Load related data
    await db.refresh(scorecard, ["behavior_scores", "power_scores", "operating_metrics", "recommendations"])

    if not scorecard.behavior_scores or not scorecard.power_scores or not scorecard.operating_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scorecard incomplete: missing components"
        )

    behavior_score = scorecard.behavior_scores[0]
    power_score = scorecard.power_scores[0]
    operating_metrics = scorecard.operating_metrics[0]

    # Determine weakest area
    areas = {
        "Behaviors": behavior_score.overall_behavior_score or 0,
        "Power Score": (power_score.total_power_score or 0) / 100,
        "Operating Metrics": (operating_metrics.overall_operating_score or 0) / 10
    }
    weakest_area = min(areas, key=areas.get)

    # Get top recommendations
    top_recommendations = scorecard.recommendations[:3] if scorecard.recommendations else []

    return {
        "ceo_scorecard_id": scorecard.id,
        "excellence_index": scorecard.ceo_excellence_index or 0,
        "behavior_score": behavior_score.overall_behavior_score or 0,
        "power_score": power_score.total_power_score or 0,
        "operating_score": operating_metrics.overall_operating_score or 0,
        "weakest_area": weakest_area,
        "top_recommendations": top_recommendations
    }


@router.get("/{scorecard_id}/recommendations", response_model=List[CEORecommendationSchema])
async def get_recommendations(
    scorecard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all recommendations for a CEO Scorecard
    """
    result = await db.execute(
        select(CEORecommendation)
        .where(CEORecommendation.ceo_scorecard_id == scorecard_id)
        .order_by(CEORecommendation.priority.desc())
    )
    recommendations = result.scalars().all()
    return recommendations

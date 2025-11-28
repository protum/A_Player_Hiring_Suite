"""Assessment service for CEO Behaviors and Power Score calculations."""

from typing import List, Dict
from ..schemas.assessment import BehaviorRatingCreate, PowerScoreResponseCreate


def calculate_ceo_overall_score(behavior_ratings: List[BehaviorRatingCreate]) -> float:
    """
    Calculate overall CEO Behaviors score.

    Based on "The CEO Next Door" - equally weight the four behaviors:
    - Decisiveness
    - Reliability
    - Adaptation
    - Engagement
    """
    if not behavior_ratings:
        return 0.0

    total_score = sum(rating.score for rating in behavior_ratings)
    return round(total_score / len(behavior_ratings), 2)


def calculate_power_scores(responses: List[PowerScoreResponseCreate]) -> Dict[str, float]:
    """
    Calculate Power Score dimensions from responses.

    Power Score = Results + Relationships + Role Model
    Each dimension scored 0-100, overall is average.
    """
    # Group responses by dimension
    dimension_scores = {
        "results": [],
        "relationships": [],
        "role_model": []
    }

    for response in responses:
        if response.response_value:
            # Convert 1-5 scale to 0-100
            normalized_score = ((response.response_value - 1) / 4) * 100
            dimension_scores[response.dimension].append(normalized_score)

    # Calculate average for each dimension
    results = {
        "results": round(sum(dimension_scores["results"]) / len(dimension_scores["results"]), 1) if dimension_scores["results"] else 0.0,
        "relationships": round(sum(dimension_scores["relationships"]) / len(dimension_scores["relationships"]), 1) if dimension_scores["relationships"] else 0.0,
        "role_model": round(sum(dimension_scores["role_model"]) / len(dimension_scores["role_model"]), 1) if dimension_scores["role_model"] else 0.0,
    }

    # Overall Power Score is the average of all three
    results["overall"] = round(
        (results["results"] + results["relationships"] + results["role_model"]) / 3,
        1
    )

    return results


def get_ceo_behavior_insights(behavior: str, score: int) -> Dict:
    """
    Get development insights based on CEO behavior scores.

    Returns recommendations for each behavior based on "The CEO Next Door".
    """
    insights = {
        "decisiveness": {
            1: {
                "level": "Critical Development Need",
                "insight": "Shows significant hesitation in decision-making. May over-analyze or seek excessive consensus.",
                "development": [
                    "Practice making smaller decisions quickly to build confidence",
                    "Set decision deadlines - commit to deciding by a specific time",
                    "Use the 70% rule - decide when you have 70% of information",
                    "Track decisions to see that most work out fine even when imperfect"
                ]
            },
            2: {
                "level": "Below Average",
                "insight": "Sometimes struggles with timely decision-making. May revisit decisions too often.",
                "development": [
                    "Distinguish between reversible and irreversible decisions",
                    "Communicate decision-making criteria to team",
                    "Practice transparent thinking while deciding"
                ]
            },
            3: {
                "level": "Average",
                "insight": "Makes decisions at reasonable pace. Could benefit from more speed and conviction.",
                "development": [
                    "Challenge yourself to cut decision time by 25%",
                    "Build stronger point of view before gathering input",
                    "Practice defending decisions with confidence"
                ]
            },
            4: {
                "level": "Above Average",
                "insight": "Generally decisive with good speed and conviction. Minor improvements possible.",
                "development": [
                    "Mentor others in decision-making frameworks",
                    "Take on higher-stakes decisions to stretch capability"
                ]
            },
            5: {
                "level": "Exceptional",
                "insight": "Highly decisive - makes tough calls quickly with conviction. Continue to refine.",
                "development": [
                    "Share decision-making frameworks with organization",
                    "Ensure speed doesn't sacrifice stakeholder buy-in where needed"
                ]
            }
        },
        "reliability": {
            1: {
                "level": "Critical Development Need",
                "insight": "Inconsistent follow-through. Commitments often missed or delayed.",
                "development": [
                    "Make fewer, more realistic commitments",
                    "Build in buffer time for all estimates",
                    "Create accountability system with check-ins",
                    "Track all commitments in single system"
                ]
            },
            2: {
                "level": "Below Average",
                "insight": "Some reliability issues. Occasionally drops balls or misses deadlines.",
                "development": [
                    "Under-promise and over-deliver",
                    "Build stronger project management systems",
                    "Communicate proactively when issues arise"
                ]
            },
            3: {
                "level": "Average",
                "insight": "Generally reliable with occasional misses. Meets most commitments.",
                "development": [
                    "Aim for 100% follow-through on commitments",
                    "Build reputation as the most reliable person in the room",
                    "Create systems to prevent any drops"
                ]
            },
            4: {
                "level": "Above Average",
                "insight": "Highly reliable. Consistently delivers on commitments.",
                "development": [
                    "Take on larger, more complex commitments",
                    "Help build reliability culture in organization"
                ]
            },
            5: {
                "level": "Exceptional",
                "insight": "Exceptionally reliable. Known for always delivering. Sets the standard.",
                "development": [
                    "Maintain this strength while taking on bigger challenges",
                    "Coach others in building reliability"
                ]
            }
        },
        "adaptation": {
            1: {
                "level": "Critical Development Need",
                "insight": "Resists change. Struggles to adapt when circumstances shift.",
                "development": [
                    "Actively seek out new approaches and perspectives",
                    "Practice reframing problems from different angles",
                    "Study examples of successful pivots and adaptations",
                    "Start with small changes to build adaptability muscle"
                ]
            },
            2: {
                "level": "Below Average",
                "insight": "Slow to adapt. Prefers status quo and familiar approaches.",
                "development": [
                    "Proactively anticipate changes rather than reacting",
                    "Build comfort with ambiguity through exposure",
                    "Seek feedback on openness to new ideas"
                ]
            },
            3: {
                "level": "Average",
                "insight": "Adapts when necessary. Could be more proactive in leading change.",
                "development": [
                    "Don't just adapt to change - drive it",
                    "Look for opportunities to innovate before being forced to",
                    "Build stronger pattern recognition for when to pivot"
                ]
            },
            4: {
                "level": "Above Average",
                "insight": "Adapts well to change. Comfortable with ambiguity and shifting direction.",
                "development": [
                    "Help others navigate change more effectively",
                    "Take on transformation challenges"
                ]
            },
            5: {
                "level": "Exceptional",
                "insight": "Thrives in change. Sees opportunities where others see obstacles.",
                "development": [
                    "Lead major transformations",
                    "Balance bold adaptation with stability where needed"
                ]
            }
        },
        "engagement": {
            1: {
                "level": "Critical Development Need",
                "insight": "Struggles to engage stakeholders. May be isolated or create friction.",
                "development": [
                    "Invest heavily in relationship building",
                    "Seek coaching on stakeholder management",
                    "Practice active listening and empathy",
                    "Schedule regular 1-on-1s with key stakeholders"
                ]
            },
            2: {
                "level": "Below Average",
                "insight": "Limited stakeholder engagement. Relationships could be stronger.",
                "development": [
                    "Map key stakeholders and engagement strategy",
                    "Increase frequency of proactive communication",
                    "Work on influence without authority skills"
                ]
            },
            3: {
                "level": "Average",
                "insight": "Adequate stakeholder engagement. Could build stronger relationships.",
                "development": [
                    "Move from adequate to exceptional in relationships",
                    "Build broader network across organization",
                    "Develop more compelling communication style"
                ]
            },
            4: {
                "level": "Above Average",
                "insight": "Strong stakeholder engagement. Builds good relationships and influence.",
                "development": [
                    "Extend influence to broader stakeholder groups",
                    "Mentor others in engagement skills"
                ]
            },
            5: {
                "level": "Exceptional",
                "insight": "Exceptional stakeholder engagement. Creates powerful coalitions and inspires others.",
                "development": [
                    "Leverage relationships to drive major initiatives",
                    "Develop next generation of leaders"
                ]
            }
        }
    }

    return insights.get(behavior, {}).get(score, {
        "level": "Not assessed",
        "insight": "No data available",
        "development": []
    })


def get_power_score_insights(dimension: str, score: float) -> Dict:
    """
    Get development insights based on Power Score dimensions.
    """
    insights = {
        "results": {
            "high": "Strong track record of delivering business results. Continue to raise the bar on outcomes.",
            "medium": "Delivers results but could increase impact. Focus on bigger, more strategic outcomes.",
            "low": "Results delivery needs improvement. Focus on setting clear goals and tracking progress."
        },
        "relationships": {
            "high": "Excellent relationship builder. Team and stakeholders trust and respect you. Leverage this strength.",
            "medium": "Solid relationships but room to deepen trust and influence. Invest more time in relationship building.",
            "low": "Relationships need significant attention. Focus on building trust, listening, and stakeholder management."
        },
        "role_model": {
            "high": "Strong values and integrity. Others look to you as an example. Continue to live your values.",
            "medium": "Generally strong values but could demonstrate more consistently. Focus on values alignment in decisions.",
            "low": "Values and integrity need strengthening. Reflect on core values and ensure actions align with words."
        }
    }

    level = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return {
        "score": score,
        "level": level,
        "insight": insights.get(dimension, {}).get(level, "No insight available")
    }

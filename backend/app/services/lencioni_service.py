"""Service layer for Ideal Team Player and Core Values assessments."""

from typing import List, Dict
from ..schemas.lencioni import VirtueRatingCreate, CoreValueRatingCreate


# Ideal Team Player Assessment Questions
IDEAL_TEAM_PLAYER_QUESTIONS = {
    "humble": [
        {"id": "H1", "text": "Compliments others without hesitation"},
        {"id": "H2", "text": "Shares credit for team successes"},
        {"id": "H3", "text": "Quick to point out contributions of others"},
        {"id": "H4", "text": "Says 'we' more often than 'I'"},
        {"id": "H5", "text": "Defines success collectively rather than individually"},
        {"id": "H6", "text": "Genuinely interested in others' ideas and opinions"},
        {"id": "H7", "text": "Admits mistakes and weaknesses readily"},
        {"id": "H8", "text": "Seeks feedback and accepts criticism"},
    ],
    "hungry": [
        {"id": "HU1", "text": "Does more than what is asked or expected"},
        {"id": "HU2", "text": "Self-motivated and diligent"},
        {"id": "HU3", "text": "Constantly thinking about next step and next opportunity"},
        {"id": "HU4", "text": "Passionate about the work and the mission"},
        {"id": "HU5", "text": "Volunteers for additional responsibilities"},
        {"id": "HU6", "text": "Feels personal responsibility for outcomes"},
        {"id": "HU7", "text": "Rarely requires management or prodding"},
        {"id": "HU8", "text": "Always looking to take on more and do more"},
    ],
    "smart": [
        {"id": "S1", "text": "Has good judgment about people and group dynamics"},
        {"id": "S2", "text": "Aware of how their words and actions impact others"},
        {"id": "S3", "text": "Tends to know what is happening in a group situation"},
        {"id": "S4", "text": "Good intuition around group dynamics and politics"},
        {"id": "S5", "text": "Knows how to deal with people in most situations"},
        {"id": "S6", "text": "Rarely says or does things that are inappropriate"},
        {"id": "S7", "text": "Adjusts interpersonal style based on audience"},
        {"id": "S8", "text": "Demonstrates empathy and concern for others"},
    ],
}


# Core Values Assessment Questions
CORE_VALUES_QUESTIONS = {
    "personal_growth": [
        {"id": "PG1", "text": "Demonstrates a commitment to continuous learning"},
        {"id": "PG2", "text": "Actively seeks opportunities to develop new skills"},
        {"id": "PG3", "text": "Embraces feedback as a growth opportunity"},
        {"id": "PG4", "text": "Shows evidence of pursuing mastery in their field"},
        {"id": "PG5", "text": "Takes initiative to improve capabilities"},
        {"id": "PG6", "text": "Reflects on experiences to extract learning"},
        {"id": "PG7", "text": "Sets and pursues ambitious personal development goals"},
        {"id": "PG8", "text": "Stays current with industry trends and best practices"},
    ],
    "harmonious_relationships": [
        {"id": "HR1", "text": "Builds trust through consistent actions"},
        {"id": "HR2", "text": "Communicates with respect even in disagreement"},
        {"id": "HR3", "text": "Actively listens and seeks to understand others"},
        {"id": "HR4", "text": "Collaborates effectively across teams"},
        {"id": "HR5", "text": "Assumes positive intent in others"},
        {"id": "HR6", "text": "Addresses conflicts constructively"},
        {"id": "HR7", "text": "Creates psychological safety for team members"},
        {"id": "HR8", "text": "Invests in building strong working relationships"},
    ],
    "problem_solving": [
        {"id": "PS1", "text": "Approaches challenges with clarity and structure"},
        {"id": "PS2", "text": "Uses creativity to find innovative solutions"},
        {"id": "PS3", "text": "Applies disciplined methodology to solving problems"},
        {"id": "PS4", "text": "Focuses on root causes rather than symptoms"},
        {"id": "PS5", "text": "Persists through difficult problems"},
        {"id": "PS6", "text": "Breaks complex problems into manageable parts"},
        {"id": "PS7", "text": "Tests solutions and learns from results"},
        {"id": "PS8", "text": "Brings both analytical and creative thinking"},
    ],
    "positive_impact": [
        {"id": "PI1", "text": "Aims to elevate clients through exceptional service"},
        {"id": "PI2", "text": "Supports colleagues' growth and success"},
        {"id": "PI3", "text": "Contributes to community and social responsibility"},
        {"id": "PI4", "text": "Creates value beyond immediate transactions"},
        {"id": "PI5", "text": "Seeks to understand and address stakeholder needs"},
        {"id": "PI6", "text": "Measures success by impact on others"},
        {"id": "PI7", "text": "Advocates for what's best for all stakeholders"},
        {"id": "PI8", "text": "Builds lasting positive relationships"},
    ],
    "financial_stewardship": [
        {"id": "FS1", "text": "Understands the business model and economics"},
        {"id": "FS2", "text": "Makes decisions with financial impact in mind"},
        {"id": "FS3", "text": "Drives revenue growth or cost efficiency"},
        {"id": "FS4", "text": "Balances short-term results with long-term value"},
        {"id": "FS5", "text": "Treats company resources as their own"},
        {"id": "FS6", "text": "Identifies opportunities to create financial value"},
        {"id": "FS7", "text": "Makes data-driven financial decisions"},
        {"id": "FS8", "text": "Demonstrates accountability for financial outcomes"},
    ],
}


def calculate_ideal_team_player_scores(
    virtue_ratings: List[VirtueRatingCreate],
) -> Dict[str, float]:
    """
    Calculate Ideal Team Player scores from virtue ratings.

    Returns dictionary with scores for each virtue and overall score.
    """
    # Group ratings by virtue
    virtue_scores = {"humble": [], "hungry": [], "smart": []}

    for rating in virtue_ratings:
        virtue_scores[rating.virtue].append(rating.response_value)

    # Calculate average for each virtue (1-5 scale)
    scores = {}
    for virtue, values in virtue_scores.items():
        if values:
            scores[f"{virtue}_score"] = round(sum(values) / len(values), 2)
        else:
            scores[f"{virtue}_score"] = 0.0

    # Overall score is average of three virtues
    scores["overall_score"] = round(
        (scores["humble_score"] + scores["hungry_score"] + scores["smart_score"]) / 3,
        2,
    )

    return scores


def determine_ideal_team_player_category(
    humble_score: float, hungry_score: float, smart_score: float
) -> str:
    """
    Determine category based on virtue scores using Lencioni's framework.

    Categories:
    - ideal_team_player: All three virtues strong (4.0+)
    - humble_only: Only humble is strong
    - hungry_only: Only hungry is strong
    - smart_only: Only smart is strong
    - humble_hungry: Humble and hungry strong, smart weak
    - humble_smart: Humble and smart strong, hungry weak
    - hungry_smart: Hungry and smart strong, humble weak
    - none: All three virtues weak (below 3.5)
    """
    threshold_high = 4.0
    threshold_low = 3.5

    humble_strong = humble_score >= threshold_high
    hungry_strong = hungry_score >= threshold_high
    smart_strong = smart_score >= threshold_high

    if humble_strong and hungry_strong and smart_strong:
        return "ideal_team_player"
    elif humble_strong and hungry_strong and not smart_strong:
        return "accidental_mess_maker"  # Lencioni term: well-meaning but lacks people skills
    elif humble_strong and smart_strong and not hungry_strong:
        return "lovable_slacker"  # Lencioni term: nice but not driving results
    elif hungry_strong and smart_strong and not humble_strong:
        return "skillful_politician"  # Lencioni term: ambitious but self-serving
    elif humble_strong and not hungry_strong and not smart_strong:
        return "pawn"  # Lencioni term: humble but ineffective
    elif hungry_strong and not humble_strong and not smart_strong:
        return "bulldozer"  # Lencioni term: driven but damaging
    elif smart_strong and not humble_strong and not hungry_strong:
        return "charmer"  # Lencioni term: likeable but not contributing
    else:
        return "ideal_mismatch"  # Lencioni term: lacking all three virtues


def get_ideal_team_player_insights(category: str) -> Dict:
    """
    Get insights and recommendations based on Ideal Team Player category.
    """
    insights = {
        "ideal_team_player": {
            "label": "Ideal Team Player",
            "description": "Possesses all three virtues: humble, hungry, and smart. This person is a strong cultural fit and will contribute positively to team dynamics.",
            "hiring_recommendation": "Strong Hire",
            "development": "Continue to develop leadership capabilities and mentor others in the three virtues.",
        },
        "accidental_mess_maker": {
            "label": "Accidental Mess-Maker",
            "description": "Humble and hungry but lacks people smarts. Well-meaning but can inadvertently create interpersonal problems.",
            "hiring_recommendation": "Caution - High Development Need",
            "development": "Focus on emotional intelligence, active listening, and awareness of impact on others. May benefit from coaching or mentorship.",
        },
        "lovable_slacker": {
            "label": "Lovable Slacker",
            "description": "Humble and people smart but lacks hunger. Nice to have around but doesn't drive results.",
            "hiring_recommendation": "Caution - Lacks Drive",
            "development": "Need to increase motivation and work ethic. Clarify expectations and create accountability structures.",
        },
        "skillful_politician": {
            "label": "Skillful Politician",
            "description": "Hungry and smart but lacks humility. Ambitious and savvy but ultimately self-serving.",
            "hiring_recommendation": "Avoid - Cultural Risk",
            "development": "Very difficult to change. Would need significant humility development through feedback and accountability.",
        },
        "pawn": {
            "label": "Pawn",
            "description": "Humble but lacks hunger and people smarts. Pleasant but ineffective contributor.",
            "hiring_recommendation": "Avoid - Limited Impact",
            "development": "Needs development in both drive and interpersonal effectiveness. Significant investment required.",
        },
        "bulldozer": {
            "label": "Bulldozer",
            "description": "Hungry but lacks humility and people smarts. Driven but damages relationships and team morale.",
            "hiring_recommendation": "Avoid - Cultural Risk",
            "development": "Needs significant work on humility and emotional intelligence. Often resistant to change.",
        },
        "charmer": {
            "label": "Charmer",
            "description": "People smart but lacks humility and hunger. Likeable but not contributing meaningfully.",
            "hiring_recommendation": "Avoid - Limited Value",
            "development": "Needs to develop work ethic and ego management. May be difficult to motivate.",
        },
        "ideal_mismatch": {
            "label": "Ideal Mismatch",
            "description": "Lacks all three virtues. Not a fit for team-based environment.",
            "hiring_recommendation": "Do Not Hire",
            "development": "Fundamental mismatch. Would require transformation across all three dimensions.",
        },
    }

    return insights.get(
        category,
        {
            "label": "Unknown Category",
            "description": "Unable to determine category",
            "hiring_recommendation": "Needs Further Assessment",
            "development": "Complete full assessment to determine development needs.",
        },
    )


def calculate_core_values_scores(
    value_ratings: List[CoreValueRatingCreate],
) -> Dict[str, float]:
    """
    Calculate Core Values scores from value ratings.

    Returns dictionary with scores for each value (0-100 scale) and overall alignment.
    """
    # Group ratings by value
    value_scores = {
        "personal_growth": [],
        "harmonious_relationships": [],
        "problem_solving": [],
        "positive_impact": [],
        "financial_stewardship": [],
    }

    for rating in value_ratings:
        value_scores[rating.value].append(rating.response_value)

    # Calculate average for each value and convert to 0-100 scale
    scores = {}
    for value, ratings in value_scores.items():
        if ratings:
            # Convert 1-5 scale to 0-100
            avg_score = sum(ratings) / len(ratings)
            scores[f"{value}_score"] = round(((avg_score - 1) / 4) * 100, 1)
        else:
            scores[f"{value}_score"] = 0.0

    # Overall alignment is average of all five values
    scores["overall_alignment_score"] = round(
        (
            scores["personal_growth_score"]
            + scores["harmonious_relationships_score"]
            + scores["problem_solving_score"]
            + scores["positive_impact_score"]
            + scores["financial_stewardship_score"]
        )
        / 5,
        1,
    )

    return scores


def determine_core_values_alignment(overall_score: float) -> str:
    """
    Determine alignment level based on overall core values score.
    """
    if overall_score >= 85:
        return "strong_fit"
    elif overall_score >= 70:
        return "good_fit"
    elif overall_score >= 50:
        return "partial_fit"
    else:
        return "poor_fit"


def get_core_values_insights(alignment_level: str, scores: Dict[str, float]) -> Dict:
    """
    Get insights and recommendations based on core values alignment.
    """
    alignment_descriptions = {
        "strong_fit": {
            "label": "Strong Cultural Fit",
            "description": "Demonstrates strong alignment with all five core values. This candidate embodies the organization's culture.",
            "hiring_recommendation": "Strong Hire",
            "onboarding_focus": "Leverage as cultural ambassador and mentor for others.",
        },
        "good_fit": {
            "label": "Good Cultural Fit",
            "description": "Demonstrates good alignment with core values with some areas for development.",
            "hiring_recommendation": "Hire",
            "onboarding_focus": "Identify specific values to reinforce during onboarding and first 90 days.",
        },
        "partial_fit": {
            "label": "Partial Cultural Fit",
            "description": "Shows alignment with some values but significant gaps in others. May struggle with cultural fit.",
            "hiring_recommendation": "Caution",
            "onboarding_focus": "Intensive cultural onboarding required. Clear expectations and frequent feedback needed.",
        },
        "poor_fit": {
            "label": "Poor Cultural Fit",
            "description": "Limited alignment with core values. High risk of cultural mismatch.",
            "hiring_recommendation": "Do Not Hire",
            "onboarding_focus": "Not recommended. Fundamental values misalignment.",
        },
    }

    insight = alignment_descriptions.get(alignment_level, {})

    # Identify strongest and weakest values
    value_names = {
        "personal_growth_score": "Personal Growth",
        "harmonious_relationships_score": "Harmonious Relationships",
        "problem_solving_score": "Problem Solving",
        "positive_impact_score": "Positive Impact",
        "financial_stewardship_score": "Financial Stewardship",
    }

    # Filter out overall score
    value_scores = {
        k: v for k, v in scores.items() if k != "overall_alignment_score"
    }

    if value_scores:
        strongest = max(value_scores, key=value_scores.get)
        weakest = min(value_scores, key=value_scores.get)

        insight["strongest_value"] = {
            "name": value_names.get(strongest, strongest),
            "score": value_scores[strongest],
        }
        insight["weakest_value"] = {
            "name": value_names.get(weakest, weakest),
            "score": value_scores[weakest],
        }

    return insight

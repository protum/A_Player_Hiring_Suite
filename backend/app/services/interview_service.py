"""Interview service for generating scripts and managing interviews."""

from typing import List, Dict
from sqlalchemy.orm import Session
from ..models.interview import Interview, JobHistory


# Standard Topgrading/Chronological Interview Questions
INTERVIEW_QUESTIONS = {
    "intro": [
        "Tell me about your educational background and what led you to your first professional role.",
        "What attracted you to this field/industry?"
    ],
    "job_overview": [
        "What were your main responsibilities in this role?",
        "Who did you report to? What was their title?",
        "Who reported to you? How large was your team?"
    ],
    "accomplishments": [
        "What were your most significant accomplishments in this role?",
        "What are you most proud of from this period?",
        "What specific results or outcomes did you achieve? (Be specific with metrics)"
    ],
    "mistakes": [
        "What mistakes or failures did you experience in this role?",
        "Looking back, what would you have done differently?",
        "What did you learn from these experiences?"
    ],
    "boss_relationship": [
        "Tell me about your relationship with your boss/supervisor.",
        "What would your boss say were your biggest strengths?",
        "What would your boss say you needed to improve?",
        "On a 1-10 scale, how would your boss rate your overall performance?"
    ],
    "team_relationships": [
        "How would your peers/colleagues describe working with you?",
        "Who were some of your key collaborators? What would they say about you?"
    ],
    "reason_for_leaving": [
        "What prompted you to leave this role?",
        "How did you go about finding your next opportunity?",
        "If we called your boss for a reference, what might they say about your departure?"
    ],
    "torc_prompts": [
        "I'll be conducting reference checks with your former supervisors. What do you think they'll tell me about your performance?",
        "What specific examples will they likely share about your strengths?",
        "What areas for development might they mention?",
        "Is there anything you'd like to clarify now that might come up in those conversations?"
    ]
}


def generate_interview_script(interview: Interview, db: Session) -> Dict:
    """
    Generate a complete chronological interview script based on job history.

    This follows the Topgrading methodology of going through each job
    chronologically and asking consistent questions about each role.
    """
    script = {
        "introduction": {
            "section": "Opening",
            "duration_minutes": 10,
            "questions": [
                "Thank you for taking the time today. We'll be conducting what's called a chronological interview, where we'll walk through your career history job by job.",
                "This helps us understand your career progression, what you've learned, and how you've grown professionally.",
                "I'll be taking notes and may ask for specific examples. Please be as detailed and candid as possible.",
                "The interview typically takes 2-3 hours. Are you comfortable with that timeframe?",
                *INTERVIEW_QUESTIONS["intro"]
            ]
        },
        "jobs": []
    }

    # Sort jobs chronologically
    jobs = sorted(interview.job_history, key=lambda x: x.start_date or "")

    for idx, job in enumerate(jobs, 1):
        job_section = {
            "job_number": idx,
            "company": job.company,
            "title": job.title,
            "dates": f"{job.start_date} to {job.end_date or 'Present'}",
            "duration_minutes": 20 if idx <= 2 else 30,  # More time for recent roles
            "question_sections": []
        }

        # Add question sections for this job
        sections = [
            ("Job Overview", INTERVIEW_QUESTIONS["job_overview"]),
            ("Key Accomplishments", INTERVIEW_QUESTIONS["accomplishments"]),
            ("Challenges & Mistakes", INTERVIEW_QUESTIONS["mistakes"]),
            ("Relationship with Boss", INTERVIEW_QUESTIONS["boss_relationship"]),
            ("Team & Peer Relationships", INTERVIEW_QUESTIONS["team_relationships"]),
            ("TORC - Threat of Reference Check", INTERVIEW_QUESTIONS["torc_prompts"]),
            ("Reason for Leaving", INTERVIEW_QUESTIONS["reason_for_leaving"]),
        ]

        for section_name, questions in sections:
            job_section["question_sections"].append({
                "section_name": section_name,
                "questions": questions,
                "notes_space": True
            })

        script["jobs"].append(job_section)

    # Add closing section
    script["closing"] = {
        "section": "Closing Questions",
        "duration_minutes": 15,
        "questions": [
            "Looking across your entire career, what patterns do you see in terms of your strengths?",
            "What types of roles or situations do you tend to thrive in?",
            "Where have you struggled or been less successful?",
            "What are you looking for in your next role?",
            "How does this opportunity align with your career goals?",
            "What questions do you have for me about this role or our organization?"
        ]
    }

    # Add red flags guidance
    script["red_flags_to_watch"] = {
        "consistency_issues": [
            "Inconsistent dates or timeline gaps",
            "Conflicting descriptions of responsibilities",
            "Changes in story when probed"
        ],
        "evasiveness": [
            "Avoiding questions about mistakes or failures",
            "Unable to provide specific metrics or examples",
            "Vague answers about boss relationships or performance ratings",
            "Defensive responses to TORC questions"
        ],
        "negative_patterns": [
            "Blaming others for failures across multiple jobs",
            "Frequent conflicts with bosses or peers",
            "Multiple short tenures without clear progression",
            "Consistent low performance ratings"
        ],
        "reference_concerns": [
            "Reluctance to provide boss names/contact info",
            "Preemptively discrediting potential references",
            "Significant anxiety around reference checks"
        ]
    }

    # Calculate total estimated time
    total_minutes = (
        script["introduction"]["duration_minutes"] +
        sum(job["duration_minutes"] for job in script["jobs"]) +
        script["closing"]["duration_minutes"]
    )
    script["estimated_total_time_minutes"] = total_minutes

    return script


def evaluate_red_flags(interview: Interview, db: Session) -> List[Dict]:
    """
    Analyze interview for potential red flags based on Topgrading principles.
    """
    red_flags = []

    # Check for pattern issues across jobs
    jobs = interview.job_history

    # Short tenure pattern
    short_tenures = [j for j in jobs if j.end_date and (j.end_date.year - j.start_date.year) < 1]
    if len(short_tenures) >= 3:
        red_flags.append({
            "type": "negative_pattern",
            "severity": "medium",
            "description": "Multiple short job tenures (less than 1 year)",
            "recommendation": "Probe deeper into reasons for leaving and pattern of job changes"
        })

    # Check for gaps in employment
    sorted_jobs = sorted(jobs, key=lambda x: x.start_date or "")
    for i in range(len(sorted_jobs) - 1):
        if sorted_jobs[i].end_date and sorted_jobs[i + 1].start_date:
            gap_days = (sorted_jobs[i + 1].start_date - sorted_jobs[i].end_date).days
            if gap_days > 90:  # More than 3 months
                red_flags.append({
                    "type": "consistency",
                    "severity": "low",
                    "description": f"Employment gap of {gap_days} days between {sorted_jobs[i].company} and {sorted_jobs[i + 1].company}",
                    "recommendation": "Ask about activities during this period"
                })

    return red_flags

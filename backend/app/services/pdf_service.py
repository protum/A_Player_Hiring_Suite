"""PDF generation service for reports and exports."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session

from ..models.candidate import Candidate


def _get_styles():
    """Get standard PDF styles."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8
    ))
    return styles


def generate_scorecard_pdf(scorecard: Any) -> bytes:
    """Generate PDF for A-Method Scorecard."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Title
    story.append(Paragraph("A-Method Role Scorecard", styles['CustomTitle']))
    story.append(Spacer(1, 0.2 * inch))

    # Role Information
    story.append(Paragraph(f"<b>Role:</b> {scorecard.role_title}", styles['CustomBody']))
    if scorecard.department:
        story.append(Paragraph(f"<b>Department:</b> {scorecard.department}", styles['CustomBody']))
    story.append(Spacer(1, 0.2 * inch))

    # Mission
    story.append(Paragraph("Mission", styles['CustomHeading']))
    story.append(Paragraph(scorecard.mission, styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Outcomes
    if scorecard.outcomes:
        story.append(Paragraph("Key Outcomes", styles['CustomHeading']))
        outcome_data = [['Priority', 'Outcome', 'Metric', 'Timeframe']]
        for outcome in scorecard.outcomes:
            outcome_data.append([
                str(outcome.priority or '-'),
                outcome.description,
                outcome.metric or '-',
                outcome.timeframe or '-'
            ])

        outcome_table = Table(outcome_data, colWidths=[0.7 * inch, 3.5 * inch, 1.5 * inch, 1.3 * inch])
        outcome_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(outcome_table)
        story.append(Spacer(1, 0.3 * inch))

    # Competencies
    if scorecard.competencies:
        story.append(Paragraph("Required Competencies", styles['CustomHeading']))
        for comp in scorecard.competencies:
            story.append(Paragraph(f"<b>{comp.name}</b>", styles['CustomBody']))
            if comp.definition:
                story.append(Paragraph(comp.definition, styles['CustomBody']))

            if comp.indicators:
                story.append(Paragraph("<i>Behavioral Indicators:</i>", styles['CustomBody']))
                for indicator in comp.indicators:
                    story.append(Paragraph(f"• {indicator.indicator}", styles['CustomBody']))

            story.append(Spacer(1, 0.15 * inch))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | A-Player Hiring Suite",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_interview_pdf(interview: Any, db: Session) -> bytes:
    """Generate PDF for Interview Report."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Get candidate info
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()

    # Title
    story.append(Paragraph("Biographical Interview Report", styles['CustomTitle']))
    story.append(Spacer(1, 0.2 * inch))

    # Candidate Information
    if candidate:
        story.append(Paragraph(f"<b>Candidate:</b> {candidate.first_name} {candidate.last_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Interview Date:</b> {interview.interview_date.strftime('%Y-%m-%d') if interview.interview_date else 'Not scheduled'}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Interviewer:</b> {interview.interviewer_name or 'Not specified'}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Status:</b> {interview.status}", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Job History
    if interview.job_history:
        story.append(Paragraph("Work History", styles['CustomHeading']))
        for job in sorted(interview.job_history, key=lambda x: x.start_date or ""):
            story.append(Paragraph(
                f"<b>{job.title}</b> at {job.company}",
                styles['CustomBody']
            ))
            story.append(Paragraph(
                f"{job.start_date} to {job.end_date or 'Present'}",
                styles['CustomBody']
            ))

            if job.responsibilities:
                story.append(Paragraph(f"<i>{job.responsibilities}</i>", styles['CustomBody']))

            # Questions and responses
            if job.questions:
                for q in job.questions:
                    if q.response:
                        story.append(Paragraph(f"<b>Q:</b> {q.question_text}", styles['CustomBody']))
                        story.append(Paragraph(f"<b>A:</b> {q.response}", styles['CustomBody']))
                        if q.rating:
                            story.append(Paragraph(f"<b>Rating:</b> {q.rating}/5", styles['CustomBody']))

            story.append(Spacer(1, 0.2 * inch))

    # Red Flags
    if interview.red_flags:
        story.append(PageBreak())
        story.append(Paragraph("Red Flags & Concerns", styles['CustomHeading']))
        flag_data = [['Type', 'Severity', 'Description']]
        for flag in interview.red_flags:
            flag_data.append([
                flag.flag_type,
                flag.severity or 'Not specified',
                flag.description
            ])

        flag_table = Table(flag_data, colWidths=[1.5 * inch, 1 * inch, 4.5 * inch])
        flag_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(flag_table)

    # Overall Assessment
    if interview.overall_rating or interview.hire_recommendation is not None:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("Overall Assessment", styles['CustomHeading']))
        if interview.overall_rating:
            story.append(Paragraph(f"<b>Rating:</b> {interview.overall_rating}", styles['CustomBody']))
        if interview.hire_recommendation is not None:
            recommendation = "Yes" if interview.hire_recommendation else "No"
            story.append(Paragraph(f"<b>Hire Recommendation:</b> {recommendation}", styles['CustomBody']))
        if interview.notes:
            story.append(Paragraph(f"<b>Notes:</b> {interview.notes}", styles['CustomBody']))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | A-Player Hiring Suite",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_ceo_assessment_pdf(assessment: Any, db: Session) -> bytes:
    """Generate PDF for CEO Behaviors Assessment."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Get subject info
    subject = db.query(Candidate).filter(Candidate.id == assessment.subject_id).first()

    # Title
    story.append(Paragraph("CEO Behaviors Leadership Assessment", styles['CustomTitle']))
    story.append(Spacer(1, 0.2 * inch))

    # Subject Information
    if subject:
        story.append(Paragraph(f"<b>Subject:</b> {subject.first_name} {subject.last_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Type:</b> {assessment.assessment_type}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Date:</b> {assessment.assessment_date.strftime('%Y-%m-%d')}", styles['CustomBody']))
    if assessment.assessor_name:
        story.append(Paragraph(f"<b>Assessor:</b> {assessment.assessor_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Overall Score:</b> {assessment.overall_score:.2f}/5.0", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Behavior Ratings
    story.append(Paragraph("The Four CEO Behaviors", styles['CustomHeading']))
    behavior_data = [['Behavior', 'Score', 'Evidence/Notes']]

    behavior_names = {
        'decisiveness': 'Decide with Speed & Conviction',
        'reliability': 'Relentless Reliability',
        'adaptation': 'Adapt Boldly',
        'engagement': 'Engage for Impact'
    }

    for rating in assessment.behavior_ratings:
        behavior_data.append([
            behavior_names.get(rating.behavior, rating.behavior),
            f"{rating.score}/5",
            rating.evidence or rating.development_notes or '-'
        ])

    behavior_table = Table(behavior_data, colWidths=[2 * inch, 0.8 * inch, 4.2 * inch])
    behavior_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(behavior_table)

    # Development Notes
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Development Recommendations", styles['CustomHeading']))
    for rating in assessment.behavior_ratings:
        if rating.development_notes:
            story.append(Paragraph(
                f"<b>{behavior_names.get(rating.behavior, rating.behavior)}:</b> {rating.development_notes}",
                styles['CustomBody']
            ))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Based on 'The CEO Next Door' methodology | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_power_score_pdf(assessment: Any, db: Session) -> bytes:
    """Generate PDF for Power Score Assessment."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Get subject info
    subject = db.query(Candidate).filter(Candidate.id == assessment.subject_id).first()

    # Title
    story.append(Paragraph("Power Score Leadership Assessment", styles['CustomTitle']))
    story.append(Spacer(1, 0.2 * inch))

    # Subject Information
    if subject:
        story.append(Paragraph(f"<b>Subject:</b> {subject.first_name} {subject.last_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Date:</b> {assessment.assessment_date.strftime('%Y-%m-%d')}", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Overall Power Score
    story.append(Paragraph(f"Overall Power Score: {assessment.overall_power_score:.1f}/100", styles['CustomHeading']))
    story.append(Spacer(1, 0.2 * inch))

    # Dimension Scores
    score_data = [
        ['Dimension', 'Score', 'Rating'],
        ['Results', f"{assessment.results_score:.1f}/100", _get_rating_label(assessment.results_score)],
        ['Relationships', f"{assessment.relationships_score:.1f}/100", _get_rating_label(assessment.relationships_score)],
        ['Role Model', f"{assessment.role_model_score:.1f}/100", _get_rating_label(assessment.role_model_score)],
    ]

    score_table = Table(score_data, colWidths=[2 * inch, 1.5 * inch, 3.5 * inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(score_table)

    # Development Plans
    if assessment.development_plans:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("Development Plan", styles['CustomHeading']))

        for plan in assessment.development_plans:
            story.append(Paragraph(
                f"<b>{plan.dimension.replace('_', ' ').title()}:</b> {plan.goal}",
                styles['CustomBody']
            ))
            if plan.action_steps:
                story.append(Paragraph(f"<i>Action Steps:</i> {plan.action_steps}", styles['CustomBody']))
            if plan.target_date:
                story.append(Paragraph(f"<i>Target Date:</i> {plan.target_date}", styles['CustomBody']))
            story.append(Spacer(1, 0.1 * inch))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Based on 'Power Score' methodology | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _get_rating_label(score: float) -> str:
    """Get rating label based on score."""
    if score >= 85:
        return "Exceptional"
    elif score >= 70:
        return "Strong"
    elif score >= 50:
        return "Adequate"
    elif score >= 30:
        return "Needs Development"
    else:
        return "Critical Gap"


def generate_ideal_team_player_pdf(assessment: Any, db: Session) -> bytes:
    """Generate PDF for Ideal Team Player assessment."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Get subject info
    subject = db.query(Candidate).filter(Candidate.id == assessment.subject_id).first()

    # Title
    story.append(Paragraph("Ideal Team Player Assessment", styles['CustomTitle']))
    story.append(Paragraph("Based on Patrick Lencioni's Framework", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Subject Information
    if subject:
        story.append(Paragraph(f"<b>Subject:</b> {subject.first_name} {subject.last_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Type:</b> {assessment.assessment_type}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Date:</b> {assessment.assessment_date.strftime('%Y-%m-%d')}", styles['CustomBody']))
    if assessment.assessor_name:
        story.append(Paragraph(f"<b>Assessor:</b> {assessment.assessor_name}", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Category and Overall Score
    from ..services.lencioni_service import get_ideal_team_player_insights
    insights = get_ideal_team_player_insights(assessment.category)
    
    story.append(Paragraph(f"<b>Category:</b> {insights['label']}", styles['CustomHeading']))
    story.append(Paragraph(insights['description'], styles['CustomBody']))
    story.append(Spacer(1, 0.2 * inch))

    # Three Virtues Scores
    story.append(Paragraph("The Three Virtues", styles['CustomHeading']))
    virtue_data = [
        ['Virtue', 'Score', 'Rating'],
        ['Humble', f"{assessment.humble_score:.2f}/5.0", _get_virtue_rating(assessment.humble_score)],
        ['Hungry', f"{assessment.hungry_score:.2f}/5.0", _get_virtue_rating(assessment.hungry_score)],
        ['Smart (People Smart)', f"{assessment.smart_score:.2f}/5.0", _get_virtue_rating(assessment.smart_score)],
        ['', '', ''],
        ['<b>Overall Score</b>', f"<b>{assessment.overall_score:.2f}/5.0</b>", ''],
    ]

    virtue_table = Table(virtue_data, colWidths=[2.5 * inch, 1.5 * inch, 3 * inch])
    virtue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(virtue_table)
    story.append(Spacer(1, 0.3 * inch))

    # Hiring Recommendation
    story.append(Paragraph("Assessment Summary", styles['CustomHeading']))
    story.append(Paragraph(f"<b>Hiring Recommendation:</b> {insights['hiring_recommendation']}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Development Focus:</b> {insights['development']}", styles['CustomBody']))

    if assessment.notes:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("<b>Additional Notes:</b>", styles['CustomBody']))
        story.append(Paragraph(assessment.notes, styles['CustomBody']))

    # Framework explanation
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("About the Three Virtues", styles['CustomHeading']))
    story.append(Paragraph("<b>Humble:</b> Lacks excessive ego, shares credit, defines success collectively", styles['CustomBody']))
    story.append(Paragraph("<b>Hungry:</b> Self-motivated, diligent, always looking to do more", styles['CustomBody']))
    story.append(Paragraph("<b>Smart (People Smart):</b> Has common sense about people and good emotional intelligence", styles['CustomBody']))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Based on 'The Ideal Team Player' by Patrick Lencioni | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_core_values_pdf(assessment: Any, db: Session) -> bytes:
    """Generate PDF for Core Values assessment."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = _get_styles()

    # Get subject info
    subject = db.query(Candidate).filter(Candidate.id == assessment.subject_id).first()

    # Title
    story.append(Paragraph("Core Values Assessment", styles['CustomTitle']))
    story.append(Paragraph("Organizational Cultural Fit Evaluation", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Subject Information
    if subject:
        story.append(Paragraph(f"<b>Subject:</b> {subject.first_name} {subject.last_name}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Type:</b> {assessment.assessment_type}", styles['CustomBody']))
    story.append(Paragraph(f"<b>Assessment Date:</b> {assessment.assessment_date.strftime('%Y-%m-%d')}", styles['CustomBody']))
    if assessment.assessor_name:
        story.append(Paragraph(f"<b>Assessor:</b> {assessment.assessor_name}", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Overall Alignment
    from ..services.lencioni_service import get_core_values_insights
    scores_dict = {
        "personal_growth_score": assessment.personal_growth_score,
        "harmonious_relationships_score": assessment.harmonious_relationships_score,
        "problem_solving_score": assessment.problem_solving_score,
        "positive_impact_score": assessment.positive_impact_score,
        "financial_stewardship_score": assessment.financial_stewardship_score,
        "overall_alignment_score": assessment.overall_alignment_score,
    }
    insights = get_core_values_insights(assessment.alignment_level, scores_dict)

    story.append(Paragraph(f"<b>Alignment Level:</b> {insights['label']}", styles['CustomHeading']))
    story.append(Paragraph(f"<b>Overall Score:</b> {assessment.overall_alignment_score:.1f}/100", styles['CustomBody']))
    story.append(Paragraph(insights['description'], styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))

    # Five Core Values Scores
    story.append(Paragraph("Core Values Scores", styles['CustomHeading']))
    values_data = [
        ['Core Value', 'Score', 'Rating'],
        ['Personal Growth', f"{assessment.personal_growth_score:.1f}/100", _get_rating_label(assessment.personal_growth_score)],
        ['Harmonious Relationships', f"{assessment.harmonious_relationships_score:.1f}/100", _get_rating_label(assessment.harmonious_relationships_score)],
        ['Problem Solving', f"{assessment.problem_solving_score:.1f}/100", _get_rating_label(assessment.problem_solving_score)],
        ['Positive Impact', f"{assessment.positive_impact_score:.1f}/100", _get_rating_label(assessment.positive_impact_score)],
        ['Financial Stewardship', f"{assessment.financial_stewardship_score:.1f}/100", _get_rating_label(assessment.financial_stewardship_score)],
    ]

    values_table = Table(values_data, colWidths=[2.5 * inch, 1.2 * inch, 3.3 * inch])
    values_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(values_table)
    story.append(Spacer(1, 0.3 * inch))

    # Key Insights
    story.append(Paragraph("Key Insights", styles['CustomHeading']))
    story.append(Paragraph(f"<b>Hiring Recommendation:</b> {insights['hiring_recommendation']}", styles['CustomBody']))
    
    if 'strongest_value' in insights:
        story.append(Paragraph(
            f"<b>Strongest Value:</b> {insights['strongest_value']['name']} ({insights['strongest_value']['score']:.1f}/100)",
            styles['CustomBody']
        ))
    if 'weakest_value' in insights:
        story.append(Paragraph(
            f"<b>Development Opportunity:</b> {insights['weakest_value']['name']} ({insights['weakest_value']['score']:.1f}/100)",
            styles['CustomBody']
        ))
    
    story.append(Paragraph(f"<b>Onboarding Focus:</b> {insights['onboarding_focus']}", styles['CustomBody']))

    if assessment.notes:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("<b>Additional Notes:</b>", styles['CustomBody']))
        story.append(Paragraph(assessment.notes, styles['CustomBody']))

    # Core Values Definitions
    story.append(PageBreak())
    story.append(Paragraph("Core Values Definitions", styles['CustomHeading']))
    
    core_values_defs = [
        ("Personal Growth", "We pursue mastery, learn continuously, and improve our capabilities every day."),
        ("Harmonious Relationships", "We foster trust, communicate with respect, and collaborate effectively."),
        ("Problem Solving", "We face challenges with clarity, creativity, and discipline, always fixing root causes."),
        ("Positive Impact", "We aim to elevate every person we serve—clients, colleagues, and communities."),
        ("Financial Stewardship", "We create value, drive revenue, and build long-term financial strength."),
    ]
    
    for value_name, definition in core_values_defs:
        story.append(Paragraph(f"<b>{value_name}:</b> {definition}", styles['CustomBody']))
        story.append(Spacer(1, 0.1 * inch))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        f"Organizational Core Values Assessment | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _get_virtue_rating(score: float) -> str:
    """Get rating label for virtue score."""
    if score >= 4.5:
        return "Exceptional"
    elif score >= 4.0:
        return "Strong"
    elif score >= 3.5:
        return "Good"
    elif score >= 3.0:
        return "Adequate"
    elif score >= 2.0:
        return "Needs Development"
    else:
        return "Weak"

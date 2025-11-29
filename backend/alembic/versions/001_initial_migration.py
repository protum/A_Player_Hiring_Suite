"""Initial migration - Create all tables

Revision ID: 001
Revises:
Create Date: 2025-11-29 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create organizations table
    op.create_table(
        'organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('size', sa.String(length=50), nullable=True),
        sa.Column('subscription_tier', sa.Enum('FREE', 'PROFESSIONAL', 'ENTERPRISE', name='subscriptiontier'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'BOARD_MEMBER', 'FOUNDER', 'CEO', 'EXECUTIVE_COACH', 'HR_MANAGER', name='userrole'), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create scorecards table
    op.create_table(
        'scorecards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role_title', sa.String(length=255), nullable=False),
        sa.Column('mission', sa.Text(), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'ACTIVE', 'ARCHIVED', name='scorecardstatus'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create scorecard_outcomes table
    op.create_table(
        'scorecard_outcomes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('metric', sa.String(length=255), nullable=True),
        sa.Column('target_value', sa.String(length=100), nullable=True),
        sa.Column('timeframe', sa.String(length=100), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['scorecard_id'], ['scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create scorecard_competencies table
    op.create_table(
        'scorecard_competencies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('behavioral_anchor_a', sa.Text(), nullable=True),
        sa.Column('behavioral_anchor_b', sa.Text(), nullable=True),
        sa.Column('behavioral_anchor_c', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['scorecard_id'], ['scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create scorecard_versions table
    op.create_table(
        'scorecard_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('changes_summary', sa.Text(), nullable=True),
        sa.Column('changed_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('snapshot_data', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['changed_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['scorecard_id'], ['scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create interviews table
    op.create_table(
        'interviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidate_name', sa.String(length=255), nullable=False),
        sa.Column('candidate_email', sa.String(length=255), nullable=True),
        sa.Column('position', sa.String(length=255), nullable=False),
        sa.Column('interviewer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='interviewstatus'), nullable=False),
        sa.Column('overall_assessment', sa.Text(), nullable=True),
        sa.Column('cqi_score', sa.Float(), nullable=True),
        sa.Column('hire_recommendation', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['interviewer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create interview_career_blocks table
    op.create_table(
        'interview_career_blocks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('position_title', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.String(length=50), nullable=True),
        sa.Column('end_date', sa.String(length=50), nullable=True),
        sa.Column('responsibilities', sa.Text(), nullable=True),
        sa.Column('accomplishments', sa.Text(), nullable=True),
        sa.Column('challenges', sa.Text(), nullable=True),
        sa.Column('reason_for_leaving', sa.Text(), nullable=True),
        sa.Column('boss_name', sa.String(length=255), nullable=True),
        sa.Column('boss_rating', sa.Integer(), nullable=True),
        sa.Column('will_call_boss', sa.Boolean(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create red_flags table
    op.create_table(
        'red_flags',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('flag_type', sa.Enum('JOB_HOPPING', 'PATTERN_OF_FAILURE', 'UNWILLING_TO_CALL_BOSS', 'VAGUE_ANSWERS', 'BLAME_OTHERS', 'LOW_BOSS_RATINGS', 'INCONSISTENT_STORY', 'OTHER', name='redflagtype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='flagseverity'), nullable=False),
        sa.Column('career_block_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['career_block_id'], ['interview_career_blocks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create reference_checks table
    op.create_table(
        'reference_checks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interview_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('career_block_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('reference_name', sa.String(length=255), nullable=False),
        sa.Column('reference_relationship', sa.String(length=255), nullable=True),
        sa.Column('contact_info', sa.String(length=255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'ATTEMPTED', 'COMPLETED', 'DECLINED', name='referencecheckstatus'), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('checked_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['career_block_id'], ['interview_career_blocks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create leadership_assessments table
    op.create_table(
        'leadership_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('subject_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_type', sa.Enum('SELF', '360', 'BOARD', 'TEAM', name='assessmenttype'), nullable=False),
        sa.Column('assessment_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('DRAFT', 'IN_PROGRESS', 'COMPLETED', name='assessmentstatus'), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('decisiveness_score', sa.Float(), nullable=True),
        sa.Column('reliability_score', sa.Float(), nullable=True),
        sa.Column('bold_adaptation_score', sa.Float(), nullable=True),
        sa.Column('engaging_for_impact_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['subject_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create behavior_ratings table
    op.create_table(
        'behavior_ratings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rater_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('behavior_dimension', sa.String(length=100), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['leadership_assessments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create raters table
    op.create_table(
        'raters',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('relationship', sa.Enum('DIRECT_REPORT', 'PEER', 'MANAGER', 'BOARD_MEMBER', 'OTHER', name='raterrelationship'), nullable=False),
        sa.Column('has_submitted', sa.Boolean(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['leadership_assessments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create evidence_items table
    op.create_table(
        'evidence_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('behavior_dimension', sa.String(length=100), nullable=False),
        sa.Column('evidence_type', sa.Enum('EXAMPLE', 'METRIC', 'OBSERVATION', 'FEEDBACK', name='evidencetype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('date_observed', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['leadership_assessments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create development_plans table
    op.create_table(
        'development_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('focus_area', sa.String(length=255), nullable=False),
        sa.Column('current_state', sa.Text(), nullable=True),
        sa.Column('desired_state', sa.Text(), nullable=True),
        sa.Column('action_steps', sa.Text(), nullable=True),
        sa.Column('success_metrics', sa.Text(), nullable=True),
        sa.Column('target_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'DEFERRED', name='developmentplanstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assessment_id'], ['leadership_assessments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create power_scores table
    op.create_table(
        'power_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('executive_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_date', sa.DateTime(), nullable=True),
        sa.Column('priorities_score', sa.Float(), nullable=False),
        sa.Column('who_score', sa.Float(), nullable=False),
        sa.Column('relationships_score', sa.Float(), nullable=False),
        sa.Column('total_power_score', sa.Float(), nullable=False),
        sa.Column('weakest_dimension', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['executive_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create priority_assessments table
    op.create_table(
        'priority_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('power_score_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clarity_of_priorities', sa.Float(), nullable=False),
        sa.Column('focus_maintenance', sa.Float(), nullable=False),
        sa.Column('team_alignment', sa.Float(), nullable=False),
        sa.Column('resource_consistency', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['power_score_id'], ['power_scores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create who_assessments table
    op.create_table(
        'who_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('power_score_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('leadership_bench_strength', sa.Float(), nullable=False),
        sa.Column('a_player_ratio', sa.Float(), nullable=False),
        sa.Column('team_gap_assessment', sa.Float(), nullable=False),
        sa.Column('delegation_efficiency', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['power_score_id'], ['power_scores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create relationship_assessments table
    op.create_table(
        'relationship_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('power_score_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('board_alignment', sa.Float(), nullable=False),
        sa.Column('cross_team_collaboration', sa.Float(), nullable=False),
        sa.Column('market_trust', sa.Float(), nullable=False),
        sa.Column('culture_health', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['power_score_id'], ['power_scores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create improvement_plans table
    op.create_table(
        'improvement_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('power_score_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dimension', sa.String(length=50), nullable=False),
        sa.Column('current_score', sa.Float(), nullable=False),
        sa.Column('target_score', sa.Float(), nullable=False),
        sa.Column('action_items', sa.Text(), nullable=True),
        sa.Column('timeline', sa.String(length=100), nullable=True),
        sa.Column('status', sa.Enum('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', name='improvementplanstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['power_score_id'], ['power_scores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ceo_scorecards table
    op.create_table(
        'ceo_scorecards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ceo_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assessment_period', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'IN_PROGRESS', 'FINALIZED', name='ceoscorecardstatus'), nullable=False),
        sa.Column('ceo_excellence_index', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('finalized_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['ceo_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ceo_behavior_scores table
    op.create_table(
        'ceo_behavior_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ceo_scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('behavior', sa.String(length=100), nullable=False),
        sa.Column('sub_dimension', sa.String(length=100), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ceo_scorecard_id'], ['ceo_scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ceo_power_scores table
    op.create_table(
        'ceo_power_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ceo_scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dimension', sa.String(length=50), nullable=False),
        sa.Column('component', sa.String(length=100), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ceo_scorecard_id'], ['ceo_scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ceo_operating_metrics table
    op.create_table(
        'ceo_operating_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ceo_scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_name', sa.String(length=255), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False),
        sa.Column('target_value', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ceo_scorecard_id'], ['ceo_scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ceo_recommendations table
    op.create_table(
        'ceo_recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ceo_scorecard_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('priority', sa.Enum('HIGH', 'MEDIUM', 'LOW', name='recommendationpriority'), nullable=False),
        sa.Column('recommendation', sa.Text(), nullable=False),
        sa.Column('rationale', sa.Text(), nullable=True),
        sa.Column('expected_impact', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ceo_scorecard_id'], ['ceo_scorecards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('ceo_recommendations')
    op.drop_table('ceo_operating_metrics')
    op.drop_table('ceo_power_scores')
    op.drop_table('ceo_behavior_scores')
    op.drop_table('ceo_scorecards')
    op.drop_table('improvement_plans')
    op.drop_table('relationship_assessments')
    op.drop_table('who_assessments')
    op.drop_table('priority_assessments')
    op.drop_table('power_scores')
    op.drop_table('development_plans')
    op.drop_table('evidence_items')
    op.drop_table('raters')
    op.drop_table('behavior_ratings')
    op.drop_table('leadership_assessments')
    op.drop_table('reference_checks')
    op.drop_table('red_flags')
    op.drop_table('interview_career_blocks')
    op.drop_table('interviews')
    op.drop_table('scorecard_versions')
    op.drop_table('scorecard_competencies')
    op.drop_table('scorecard_outcomes')
    op.drop_table('scorecards')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('organizations')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS recommendationpriority')
    op.execute('DROP TYPE IF EXISTS ceoscorecardstatus')
    op.execute('DROP TYPE IF EXISTS improvementplanstatus')
    op.execute('DROP TYPE IF EXISTS developmentplanstatus')
    op.execute('DROP TYPE IF EXISTS evidencetype')
    op.execute('DROP TYPE IF EXISTS raterrelationship')
    op.execute('DROP TYPE IF EXISTS assessmentstatus')
    op.execute('DROP TYPE IF EXISTS assessmenttype')
    op.execute('DROP TYPE IF EXISTS referencecheckstatus')
    op.execute('DROP TYPE IF EXISTS flagseverity')
    op.execute('DROP TYPE IF EXISTS redflagtype')
    op.execute('DROP TYPE IF EXISTS interviewstatus')
    op.execute('DROP TYPE IF EXISTS scorecardstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS subscriptiontier')

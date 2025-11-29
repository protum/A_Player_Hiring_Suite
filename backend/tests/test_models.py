"""
Tests for database models
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.models.user import User, Organization, UserRole, SubscriptionTier
from app.models.scorecard import Scorecard, ScorecardOutcome, ScorecardCompetency
from app.models.interview import Interview, InterviewCareerBlock
from app.core.security import get_password_hash


@pytest.mark.asyncio
async def test_create_organization(async_session: AsyncSession):
    """Test creating an organization"""
    org = Organization(
        name="Test Company",
        industry="Technology",
        size="50-200",
        subscription_tier=SubscriptionTier.PROFESSIONAL
    )
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    assert org.id is not None
    assert org.name == "Test Company"
    assert org.subscription_tier == SubscriptionTier.PROFESSIONAL


@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    """Test creating a user"""
    # Create organization first
    org = Organization(name="Test Org")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    # Create user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        role=UserRole.HR_MANAGER,
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == UserRole.HR_MANAGER
    assert user.is_active is True


@pytest.mark.asyncio
async def test_create_scorecard_with_outcomes(async_session: AsyncSession):
    """Test creating a scorecard with outcomes"""
    # Create org and user
    org = Organization(name="Test Org")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create scorecard
    scorecard = Scorecard(
        role_title="Engineer",
        mission="Build great products",
        organization_id=org.id,
        created_by_id=user.id,
        status="ACTIVE",
        version=1
    )
    async_session.add(scorecard)
    await async_session.commit()
    await async_session.refresh(scorecard)

    # Add outcome
    outcome = ScorecardOutcome(
        scorecard_id=scorecard.id,
        description="Ship 3 features",
        metric="Features",
        target_value="3",
        timeframe="Q1 2024",
        display_order=1
    )
    async_session.add(outcome)
    await async_session.commit()

    assert scorecard.id is not None
    assert outcome.scorecard_id == scorecard.id


@pytest.mark.asyncio
async def test_create_interview(async_session: AsyncSession):
    """Test creating an interview"""
    # Create user
    org = Organization(name="Test Org")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create interview
    interview = Interview(
        candidate_name="John Doe",
        candidate_email="john@example.com",
        position="Senior Engineer",
        interviewer_id=user.id,
        status="SCHEDULED"
    )
    async_session.add(interview)
    await async_session.commit()
    await async_session.refresh(interview)

    assert interview.id is not None
    assert interview.candidate_name == "John Doe"
    assert interview.status == "SCHEDULED"


@pytest.mark.asyncio
async def test_user_organization_relationship(async_session: AsyncSession):
    """Test relationship between user and organization"""
    org = Organization(name="Test Company")
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    user1 = User(
        email="user1@example.com",
        hashed_password=get_password_hash("pass123"),
        full_name="User One",
        organization_id=org.id
    )
    user2 = User(
        email="user2@example.com",
        hashed_password=get_password_hash("pass123"),
        full_name="User Two",
        organization_id=org.id
    )

    async_session.add(user1)
    async_session.add(user2)
    await async_session.commit()

    # Refresh to load relationships
    await async_session.refresh(org)

    # Note: In async SQLAlchemy, relationships need to be explicitly loaded
    # This test verifies the foreign key relationship works
    assert user1.organization_id == org.id
    assert user2.organization_id == org.id

"""
Tests for scorecard endpoints
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.models.user import User, Organization
from app.models.scorecard import Scorecard
from app.core.security import get_password_hash


@pytest.mark.asyncio
async def test_create_scorecard(
    client: AsyncClient,
    async_session: AsyncSession,
    test_user_data: dict,
    test_organization_data: dict,
    test_scorecard_data: dict
):
    """Test creating a scorecard"""
    # Create organization
    org = Organization(**test_organization_data)
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    # Create user
    user = User(
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        full_name=test_user_data["full_name"],
        role="hr_manager",
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    # Create scorecard
    response = await client.post(
        "/api/v1/scorecards",
        json=test_scorecard_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["role_title"] == test_scorecard_data["role_title"]
    assert data["mission"] == test_scorecard_data["mission"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_scorecards_list(
    client: AsyncClient,
    async_session: AsyncSession,
    test_user_data: dict,
    test_organization_data: dict
):
    """Test getting list of scorecards"""
    # Create organization
    org = Organization(**test_organization_data)
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    # Create user
    user = User(
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        full_name=test_user_data["full_name"],
        role="hr_manager",
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create scorecards
    scorecard1 = Scorecard(
        role_title="Engineer",
        mission="Build products",
        organization_id=org.id,
        created_by_id=user.id,
        status="ACTIVE",
        version=1
    )
    scorecard2 = Scorecard(
        role_title="Designer",
        mission="Design interfaces",
        organization_id=org.id,
        created_by_id=user.id,
        status="ACTIVE",
        version=1
    )
    async_session.add(scorecard1)
    async_session.add(scorecard2)
    await async_session.commit()

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    # Get scorecards
    response = await client.get(
        "/api/v1/scorecards",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_scorecard_by_id(
    client: AsyncClient,
    async_session: AsyncSession,
    test_user_data: dict,
    test_organization_data: dict
):
    """Test getting a specific scorecard"""
    # Create organization
    org = Organization(**test_organization_data)
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    # Create user
    user = User(
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        full_name=test_user_data["full_name"],
        role="hr_manager",
        organization_id=org.id
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create scorecard
    scorecard = Scorecard(
        role_title="Engineer",
        mission="Build products",
        organization_id=org.id,
        created_by_id=user.id,
        status="ACTIVE",
        version=1
    )
    async_session.add(scorecard)
    await async_session.commit()
    await async_session.refresh(scorecard)

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    # Get scorecard
    response = await client.get(
        f"/api/v1/scorecards/{scorecard.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role_title"] == "Engineer"
    assert data["mission"] == "Build products"

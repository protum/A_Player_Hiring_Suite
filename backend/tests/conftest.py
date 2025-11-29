"""
Pytest configuration and fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from app.core.security import get_password_hash


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://aplayer:aplayer123@localhost:5432/aplayer_hiring_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_engine():
    """Create async test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create async test database session"""
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client"""
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "hr_manager"
    }


@pytest.fixture
def test_organization_data():
    """Sample organization data for testing"""
    return {
        "name": "Test Company",
        "industry": "Technology",
        "size": "50-200",
        "subscription_tier": "professional"
    }


@pytest.fixture
def test_scorecard_data():
    """Sample scorecard data for testing"""
    return {
        "role_title": "Senior Software Engineer",
        "mission": "Build scalable systems that serve millions of users",
        "outcomes": [
            {
                "description": "Ship 3 major features per quarter",
                "metric": "Feature delivery",
                "target_value": "3",
                "timeframe": "Q1 2024"
            }
        ],
        "competencies": [
            {
                "name": "System Design",
                "behavioral_anchor_a": "Designs simple, maintainable systems",
                "behavioral_anchor_b": "Considers scalability and performance",
                "behavioral_anchor_c": "Anticipates future requirements"
            }
        ]
    }

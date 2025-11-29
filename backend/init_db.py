#!/usr/bin/env python3
"""
Database initialization script
Creates tables and optionally adds seed data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import async_engine, Base
from app.core.security import get_password_hash
from app.models import *  # Import all models


async def init_database(drop_existing: bool = False):
    """
    Initialize the database schema

    Args:
        drop_existing: If True, drop all existing tables before creating new ones
    """
    print("🔧 Initializing database...")

    async with async_engine.begin() as conn:
        if drop_existing:
            print("⚠️  Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)

        print("📊 Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized successfully!")


async def seed_data():
    """
    Add seed data for development/testing
    """
    from app.core.database import AsyncSessionLocal
    from app.models.user import User, Organization, UserRole, SubscriptionTier

    print("🌱 Seeding database with sample data...")

    async with AsyncSessionLocal() as session:
        try:
            # Check if data already exists
            result = await session.execute(text("SELECT COUNT(*) FROM organizations"))
            count = result.scalar()

            if count > 0:
                print("⚠️  Database already contains data. Skipping seed.")
                return

            # Create sample organization
            org = Organization(
                name="Demo Company",
                industry="Technology",
                size="50-200",
                subscription_tier=SubscriptionTier.PROFESSIONAL
            )
            session.add(org)
            await session.flush()

            # Create sample admin user
            admin_user = User(
                email="admin@demo.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN,
                organization_id=org.id,
                is_active=True
            )
            session.add(admin_user)

            # Create sample HR manager
            hr_user = User(
                email="hr@demo.com",
                hashed_password=get_password_hash("hr123"),
                full_name="HR Manager",
                role=UserRole.HR_MANAGER,
                organization_id=org.id,
                is_active=True
            )
            session.add(hr_user)

            # Create sample CEO
            ceo_user = User(
                email="ceo@demo.com",
                hashed_password=get_password_hash("ceo123"),
                full_name="CEO Demo",
                role=UserRole.CEO,
                organization_id=org.id,
                is_active=True
            )
            session.add(ceo_user)

            await session.commit()

            print("✅ Seed data created successfully!")
            print("\n📋 Sample Accounts:")
            print("   Admin:      admin@demo.com / admin123")
            print("   HR Manager: hr@demo.com / hr123")
            print("   CEO:        ceo@demo.com / ceo123")

        except Exception as e:
            print(f"❌ Error seeding data: {e}")
            await session.rollback()
            raise


async def check_connection():
    """
    Test database connection
    """
    print("🔍 Testing database connection...")

    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def main():
    """
    Main initialization function
    """
    import argparse

    parser = argparse.ArgumentParser(description="Initialize A-Player Hiring Suite database")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop existing tables before creating new ones"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Add seed data after initialization"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check database connection"
    )

    args = parser.parse_args()

    # Check connection
    if not await check_connection():
        print("\n⚠️  Please ensure PostgreSQL is running and DATABASE_URL is configured correctly.")
        print("   Check your .env file or environment variables.")
        return 1

    if args.check:
        return 0

    # Initialize database
    await init_database(drop_existing=args.drop)

    # Seed data if requested
    if args.seed:
        await seed_data()

    print("\n🎉 Database setup complete!")

    # Cleanup
    await async_engine.dispose()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

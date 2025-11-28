"""
User and Organization models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    BOARD_MEMBER = "board_member"
    FOUNDER = "founder"
    CEO = "ceo"
    EXECUTIVE_COACH = "executive_coach"
    HR_MANAGER = "hr_manager"


class SubscriptionTier(str, enum.Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class Organization(Base):
    """Organization/Company model"""
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    size = Column(String(50))
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    scorecards = relationship("Scorecard", back_populates="organization", cascade="all, delete-orphan")
    ceo_scorecards = relationship("CEOScorecard", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization {self.name}>"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.HR_MANAGER, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    scorecards_created = relationship("Scorecard", back_populates="created_by", foreign_keys="Scorecard.created_by_id")
    interviews_conducted = relationship("Interview", back_populates="interviewer", foreign_keys="Interview.interviewer_id")
    leadership_assessments_subject = relationship(
        "LeadershipAssessment",
        back_populates="subject",
        foreign_keys="LeadershipAssessment.subject_id"
    )
    power_scores = relationship("PowerScore", back_populates="executive", foreign_keys="PowerScore.executive_id")
    ceo_scorecards = relationship("CEOScorecard", back_populates="ceo", foreign_keys="CEOScorecard.ceo_id")

    def __repr__(self):
        return f"<User {self.email}>"

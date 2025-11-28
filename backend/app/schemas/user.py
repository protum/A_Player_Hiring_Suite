"""
User and authentication schemas
"""
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, SubscriptionTier


# Organization schemas
class OrganizationBase(BaseModel):
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    subscription_tier: Optional[SubscriptionTier] = None


class Organization(OrganizationBase):
    id: UUID4
    subscription_tier: SubscriptionTier
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.HR_MANAGER


class UserCreate(UserBase):
    password: str
    organization_id: Optional[UUID4] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: UUID4
    organization_id: Optional[UUID4]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[UUID4] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

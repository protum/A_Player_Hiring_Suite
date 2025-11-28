"""Candidate model."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .base import Base
import uuid


class Candidate(Base):
    """Candidate entity representing a person being assessed."""

    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    current_title = Column(String)
    linkedin_url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Candidate {self.first_name} {self.last_name}>"

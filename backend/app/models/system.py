"""System models for settings and history."""

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from .base import Base


class AppSetting(Base):
    """Application settings and configuration."""

    __tablename__ = "app_settings"

    key = Column(String, primary_key=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Setting: {self.key}>"


class ExportHistory(Base):
    """History of data exports."""

    __tablename__ = "export_history"

    id = Column(String, primary_key=True)
    export_type = Column(String, nullable=False)  # pdf, json, sqlite_backup
    file_path = Column(String)
    exported_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Export: {self.export_type} - {self.exported_at}>"

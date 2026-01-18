"""SQLAlchemy models for PostgreSQL database"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .postgres import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    RECRUITER = "recruiter"
    ADMIN = "admin"


class ApplicationStatus(str, enum.Enum):
    """Application status enumeration"""
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    jobs = relationship("Job", back_populates="creator")
    candidate = relationship("Candidate", back_populates="user", uselist=False)


class Job(Base):
    """Job posting model"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    salary = Column(String(100))
    requirements_json = Column(JSON)  # Stores JobRequirement as JSON
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Candidate(Base):
    """Candidate model"""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50))
    skills_json = Column(JSON)  # List of skills as JSON
    resume_id = Column(String(100))  # Reference to MongoDB resume document
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="candidate")
    applications = relationship("Application", back_populates="candidate")


class Application(Base):
    """Job application model"""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    evaluations = relationship("Evaluation", back_populates="application")


class Evaluation(Base):
    """ATS evaluation model"""
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    ats_score = Column(Float, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)
    skill_match_score = Column(Float)
    education_score = Column(Float)
    experience_score = Column(Float)
    keyword_match_score = Column(Float)
    format_score = Column(Float)
    matched_skills_json = Column(JSON)
    missing_skills_json = Column(JSON)
    feedback_id = Column(String(100))  # Reference to MongoDB feedback document
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="evaluations")

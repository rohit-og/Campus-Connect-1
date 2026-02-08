"""
Pydantic schemas for Aptitude Engine API
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .models import DifficultyLevel


# --- Test & Question (for start test) ---

class QuestionResponse(BaseModel):
    """Question as returned when starting a test (no correct answer exposed in start flow)"""
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: Optional[str] = None  # Not sent to client in start; used internally
    difficulty_level: Optional[DifficultyLevel] = None

    class Config:
        from_attributes = True


class TestInfo(BaseModel):
    """Test metadata"""
    id: int
    title: str
    description: Optional[str] = None
    duration_minutes: int
    total_questions: int

    class Config:
        from_attributes = True


class TestStartResponse(BaseModel):
    """Response when starting a test"""
    attempt_id: int
    test: TestInfo
    questions: List[QuestionResponse]
    started_at: datetime
    duration_minutes: int


# --- Submit ---

class AnswerItem(BaseModel):
    """Single answer in a submission"""
    question_id: int
    selected_option: str  # 'A', 'B', 'C', or 'D'


class TestSubmissionRequest(BaseModel):
    """Request body for submitting a test"""
    answers: List[AnswerItem]


class TestSubmissionResponse(BaseModel):
    """Response after submitting a test"""
    attempt_id: int
    score: float
    total_questions: int
    correct_answers: int
    time_taken: int
    submitted_at: datetime


# --- Leaderboard ---

class LeaderboardEntry(BaseModel):
    """Single entry on the leaderboard"""
    rank: int
    user_id: int
    score: float
    time_taken: int
    submitted_at: Optional[datetime] = None


class LeaderboardResponse(BaseModel):
    """Leaderboard for a test"""
    test_id: int
    test_title: str
    entries: List[LeaderboardEntry]
    total_participants: int


# --- My rank ---

class StudentRankResponse(BaseModel):
    """Student's rank info for a test"""
    test_id: int
    test_title: str
    user_id: int
    rank: Optional[int] = None
    score: Optional[float] = None
    time_taken: Optional[int] = None
    percentile: Optional[float] = None
    total_participants: int
    submitted_at: Optional[datetime] = None


# --- Detailed results ---

class QuestionResultDetail(BaseModel):
    """Detailed result for a single question"""
    question_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str  # 'A', 'B', 'C', or 'D'
    selected_option: Optional[str] = None  # What the student selected, or None if skipped
    is_correct: bool
    difficulty_level: str

    class Config:
        from_attributes = True


class DetailedTestResultsResponse(BaseModel):
    """Detailed results showing all questions with correct/incorrect answers"""
    attempt_id: int
    test_id: int
    test_title: str
    user_id: int
    score: float
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    skipped_questions: int
    time_taken: int  # seconds
    submitted_at: datetime
    questions: List[QuestionResultDetail]

"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    goal: Optional[str] = None

class QuestionRequest(BaseModel):
    user_id: int
    question: str

class QuizGenerateRequest(BaseModel):
    user_id: int
    topic: str
    num_questions: int = 5

class QuizSubmitRequest(BaseModel):
    user_id: int
    topic: str
    answers: List[int]
    correct_answers: List[int]

class SkillAnalyzeRequest(BaseModel):
    user_id: int
    user_skills: List[str]
    target_role: str

class RoadmapRequest(BaseModel):
    user_id: int
    target_role: str
    missing_skills: List[str]

class MCQQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int

class ChatMessage(BaseModel):
    user_id: int
    message: str

class ChatHistoryResponse(BaseModel):
    id: int
    message: str
    is_user: bool
    timestamp: str

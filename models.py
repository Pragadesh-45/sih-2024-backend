from pydantic import BaseModel
from typing import List, Optional

# User model
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: str  # trainer, institution, regulatory body

# Institution model
class Institution(BaseModel):
    id: str
    name: str
    location: str
    average_score: float
    user_id: str

# Session model
class Session(BaseModel):
    id: str
    user_id: str
    institution_id: str
    name: str
    no_of_slots: int
    average_eng_score: float

# Slot model
class Slot(BaseModel):
    id: str
    title: str
    date: str
    time_from: str
    time_to: str
    engagement_score: float
    report: Optional[str]
    session_id: str
    user_id: str

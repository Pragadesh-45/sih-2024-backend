from pydantic import BaseModel
from typing import List, Optional

# User model 
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: str  

# Institution model
class Institution(BaseModel):
    id: str
    name: str
    location: str
    average_score: float
    user_id: str  
    email: str
    trainers: List[str] 
    sessions: List[str] 

# Trainer model
class Trainer(BaseModel):
    id: str
    name: str
    email: str
    password: str
    institution_id: str  
    sessions: List[str]  
    slots: List[str]  

# Session model
class Session(BaseModel):
    id: str
    trainer_ids: List[str]  
    institution_id: str
    name: str
    no_of_slots: int  
    average_eng_score: float
    slots: List[str]  

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
    trainer_id: str  

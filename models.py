from pydantic import BaseModel,Field,validator
from typing import List, Optional
import uuid

# User model 
class User(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))   
    id: str = None
    name: str
    email: str
    password: str
    role: str =None
# Institution model
class Institution(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))   
    id: str = None
    name: str
    location: str
    average_score: float = 0.0
    user_id: str=None  
    email: str
    password:str =None
    trainers: List[str] =[]
    sessions: List[str]=[]
    status:str = None 



# Trainer model
class Trainer(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    id: str = None
    name: str
    email: str
    password: str = None
    institution_id: str  
    sessions: List[str] = []  
    slots: List[str] = [] 

# Session model
class Session(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    id: str = None
    trainer_ids: List[str]  
    institution_id: str
    name: str
    no_of_slots: int  
    average_eng_score: float = None
    slots: List[str]  

# Slot model
class Slot(BaseModel):
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))  
    id: str = None
    title: str
    date: str
    time_from: str
    time_to: str
    engagement_score: float =None
    report: Optional[str] =""
    session_id: str 
    trainer_id: str  

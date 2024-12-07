from fastapi import APIRouter, HTTPException
from database import trainers_collection  
from models import Trainer  

router = APIRouter()

from emailservice import send_email  

@router.post("/trainers/")
async def create_trainer(trainer: Trainer):
    existing_trainer = trainers_collection.find_one({"email": trainer.email})
    if existing_trainer:
        raise HTTPException(status_code=400, detail="Trainer with this email already exists")
    
    trainers_collection.insert_one(trainer.dict())
    
    subject = "Welcome to Our Platform"
    message = f"""
    Hello {trainer.name},
    
    Welcome to our platform! We're excited to have you on board. 
    As a trainer, you can now manage your sessions, view your schedules, and interact with institutions seamlessly.

    If you have any questions or need support, feel free to reach out to us.

    Best regards,
    The Team
    """
    
    try:
        send_email(trainer.email, subject, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending welcome email: {str(e)}")
    
    return {"message": "Trainer created successfully and welcome email sent"}


@router.get("/trainers/")
async def get_trainers():
    trainers = list(trainers_collection.find({}, {"_id": 0}))
    return trainers


@router.get("/trainers/{trainer_id}")
async def get_trainer(trainer_id: str):
    trainer = trainers_collection.find_one({"id": trainer_id}, {"_id": 0})
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer



@router.put("/trainers/{trainer_id}")
async def update_trainer(trainer_id: str, trainer: Trainer):
    result = trainers_collection.update_one({"id": trainer_id}, {"$set": trainer.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return {"message": "Trainer updated successfully"}

@router.delete("/trainers/{trainer_id}")
async def delete_trainer(trainer_id: str):
    result = trainers_collection.delete_one({"id": trainer_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return {"message": "Trainer deleted successfully"}

from fastapi import APIRouter, HTTPException
from database import trainers_collection,institutions_collection  
from models import Trainer  
import secrets
from emailservice import send_email


def generate_random_password(length=8):
    return secrets.token_urlsafe(length)[:length]


router = APIRouter()


@router.post("/trainers/")
async def create_trainer(trainer: Trainer):
    # Check if institution_id is provided
    if not trainer.institution_id:
        raise HTTPException(status_code=400, detail="Institution ID is required")
    
    # Validate if the institution exists
    institution = institutions_collection.find_one({"id": trainer.institution_id})
    if not institution:
        raise HTTPException(status_code=400, detail="Institution does not exist")
    
    # Check for existing email or ID
    existing_trainer = trainers_collection.find_one({"email": trainer.email})
    existing_trainer_id = trainers_collection.find_one({"id": trainer.id})
    if existing_trainer:
        raise HTTPException(status_code=400, detail="Trainer with this email already exists")
    if existing_trainer_id:
        raise HTTPException(status_code=400, detail="Trainer with this Trainer ID already exists")
    
    # Generate random password
    random_password = generate_random_password()
    
    # Store the plain-text password (not recommended)
    trainer.password = random_password  # Store the password directly
    
    # Insert the trainer into the database
    trainers_collection.insert_one(trainer.dict())
    
    # Send welcome email with the generated password
    subject = "Welcome to Our Platform"
    message = f"""
    Hello {trainer.name},
    
    Welcome to our platform! Your trainer account has been successfully created.
    Below are your login details:
    
    - Email: {trainer.email}
    - Password: {random_password}
    
    Institution: {institution.get('name', 'Unknown')}
    
    Please change your password upon logging in for the first time.

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

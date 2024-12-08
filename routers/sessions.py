from fastapi import APIRouter, HTTPException
from database import sessions_collection, trainers_collection,slots_collection
from models import Session,Slot
from emailservice import send_email


router = APIRouter()

@router.post("/sessions/")
@router.post("/sessions/")
async def create_session(session: Session):
    sessions_collection.insert_one(session.dict())
    
    trainer_emails = []
    for trainer_id in session.trainer_ids:
        trainer = trainers_collection.find_one({"id": trainer_id})
        if not trainer:
            raise HTTPException(status_code=404, detail=f"Trainer with ID {trainer_id} not found")
        
        trainer_email = trainer.get("email")
        if not trainer_email:
            raise HTTPException(status_code=404, detail=f"Email for Trainer ID {trainer_id} not found")
        
        trainer_emails.append((trainer_email, trainer.get("name")))
    
    subject = "New Session Assigned"
    
    for trainer_email, trainer_name in trainer_emails:
        message = f"""
        Hello {trainer_name},
        
        A new session has been assigned to you:
        - Session ID: {session.id}
        - Session Name: {session.name}
        - Number of Slots: {session.no_of_slots}
        - Institution ID: {session.institution_id}

        Please log in to your account to view more details.

        Regards,
        Your Team
        """
        
        try:
            send_email(trainer_email, subject, message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error sending email to {trainer_email}: {str(e)}")
    
    return {"message": "Session created and emails sent to all trainers successfully"}

@router.get("/sessions/")
async def get_sessions():
    return list(sessions_collection.find({}, {"_id": 0}))

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    session = sessions_collection.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/sessions/{session_id}")
async def update_session(session_id: str, session: Session):
    result = sessions_collection.update_one({"id": session_id}, {"$set": session.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session updated successfully"}

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    result = sessions_collection.delete_one({"id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}

@router.get("/sessions/{session_id}/slots")
async def get_slots_for_session(session_id: str):
    # First, check if the session exists
    session = sessions_collection.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Now, fetch slots from the slots collection that belong to this session
    slots = slots_collection.find({"session_id": session_id}, {"_id": 0})
    
    # If no slots are found, raise an error
    slots_list = list(slots)
    if not slots_list:
        raise HTTPException(status_code=404, detail="No slots found for this session")
    return slots_list

@router.patch("/sessions/{session_id}/slots")
async def update_slots_for_session(session_id: str, slot: Slot):
    # First, check if the session exists
    session = sessions_collection.find_one({"id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Prepare the slot data to be updated or added
    # Here, slot.dict(exclude_unset=True) will ensure that only fields provided in the request are updated.
    slot_data = slot.dict(exclude_unset=True)
    
    # Add or update the slot for the given session
    # If slot ID exists, we update; if not, a new slot is inserted
    if "id" in slot_data:
        result = slots_collection.update_one({"id": slot_data["id"], "session_id": session_id}, {"$set": slot_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Slot not found for the given session")
        return {"message": "Slot updated successfully"}
    else:
        # Insert the new slot if it does not exist yet
        slot_data["session_id"] = session_id  # Ensure the session_id is set
        slots_collection.insert_one(slot_data)
        return {"message": "Slot created successfully"}

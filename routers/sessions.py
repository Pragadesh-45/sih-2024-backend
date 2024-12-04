from fastapi import APIRouter, HTTPException
from database import sessions_collection
from models import Session

router = APIRouter()

@router.post("/sessions/")
async def create_session(session: Session):
    sessions_collection.insert_one(session.dict())
    return {"message": "Session created successfully"}

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

from fastapi import APIRouter, HTTPException
from database import institutions_collection,trainers_collection,sessions_collection
from models import Institution

router = APIRouter()

@router.post("/institutions/")
async def create_institution(institution: Institution):
    institutions_collection.insert_one(institution.dict())
    return {"message": "Institution created successfully"}

@router.get("/institutions/")
async def get_institutions():
    return list(institutions_collection.find({}, {"_id": 0}))

@router.get("/institutions/{institution_id}")
async def get_institution(institution_id: str):
    institution = institutions_collection.find_one({"id": institution_id}, {"_id": 0})
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution

@router.put("/institutions/{institution_id}")
async def update_institution(institution_id: str, institution: Institution):
    result = institutions_collection.update_one({"id": institution_id}, {"$set": institution.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Institution not found")
    return {"message": "Institution updated successfully"}

@router.delete("/institutions/{institution_id}")
async def delete_institution(institution_id: str):
    result = institutions_collection.delete_one({"id": institution_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Institution not found")
    return {"message": "Institution deleted successfully"}

@router.get("/institutions/{institution_id}/trainers")
async def get_trainers_for_institution(institution_id: str):
    # Fetch the institution to check if it exists
    institution = institutions_collection.find_one({"id": institution_id})
    print(institution)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    # Assuming each institution stores trainer IDs (or references)
    trainer_ids = institution.get("trainers", [])

    
    if not trainer_ids:
        raise HTTPException(status_code=404, detail="No trainers found for this institution")
    
    # Fetch trainers associated with the institution
    trainers = list(trainers_collection.find({"id": {"$in": trainer_ids}}, {"_id": 0}))
    
    if not trainers:
        raise HTTPException(status_code=404, detail="No trainers found")
    
    return trainers


@router.get("/institutions/{institution_id}/sessions")
async def get_sessions_for_institution(institution_id: str):
    # Fetch the institution to check if it exists
    institution = institutions_collection.find_one({"id": institution_id})
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    # Fetch sessions associated with the institution
    sessions = list(sessions_collection.find({"institution_id": institution_id}, {"_id": 0}))
    
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this institution")
    
    return sessions

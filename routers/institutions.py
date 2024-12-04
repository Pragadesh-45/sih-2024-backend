from fastapi import APIRouter, HTTPException
from database import institutions_collection
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

from fastapi import APIRouter, HTTPException
from database import slots_collection
from models import Slot

router = APIRouter()

@router.post("/slots/")
async def create_slot(slot: Slot):
    slots_collection.insert_one(slot.dict())
    return {"message": "Slot created successfully"}

@router.get("/slots/")
async def get_slots():
    return list(slots_collection.find({}, {"_id": 0}))

@router.get("/slots/{slot_id}")
async def get_slot(slot_id: str):
    slot = slots_collection.find_one({"id": slot_id}, {"_id": 0})
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

@router.put("/slots/{slot_id}")
async def update_slot(slot_id: str, slot: Slot):
    result = slots_collection.update_one({"id": slot_id}, {"$set": slot.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Slot not found")
    return {"message": "Slot updated successfully"}

@router.delete("/slots/{slot_id}")
async def delete_slot(slot_id: str):
    result = slots_collection.delete_one({"id": slot_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Slot not found")
    return {"message": "Slot deleted successfully"}

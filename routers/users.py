from fastapi import APIRouter, HTTPException
from database import users_collection
from models import User

router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    users_collection.insert_one(user.dict())
    return {"message": "User created successfully"}

@router.get("/users/")
async def get_users():
    return list(users_collection.find({}, {"_id": 0}))

@router.get("/users/{email}")
async def get_user(email: str):
    user = users_collection.find_one({"email": email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    result = users_collection.update_one({"id": user_id}, {"$set": user.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = users_collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

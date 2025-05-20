from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from app.db.mongodb import get_db
from app.core.security import get_current_user
from bson.objectid import ObjectId

# Define Pydantic models for request/response validation
class ResumeData(BaseModel):
    user_id: str
    resume_data: Dict[str, Any]

class ResumeResponse(BaseModel):
    id: str
    user_id: str
    resume_data: Dict[str, Any]

# Create FastAPI router
router = APIRouter()

@router.post("/resumes", response_model=Dict[str, str], status_code=201)
async def upload_resume(data: ResumeData):
    db = get_db()
    resume = {
        'user_id': data.user_id,
        'resume_data': data.resume_data,
        'uploaded_at': datetime.utcnow()
    }
    result = db.resumes.insert_one(resume)
    return {"id": str(result.inserted_id)}

@router.get("/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str):
    db = get_db()
    resume = db.resumes.find_one({'_id': ObjectId(resume_id)})
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {
        "id": str(resume['_id']), 
        "user_id": resume['user_id'], 
        "resume_data": resume['resume_data']
    }

@router.get("/resumes/user/{user_id}", response_model=List[ResumeResponse])
async def get_user_resumes(user_id: str):
    db = get_db()
    resumes = list(db.resumes.find({'user_id': user_id}))
    return [
        {
            "id": str(resume['_id']), 
            "user_id": resume['user_id'], 
            "resume_data": resume['resume_data']
        } 
        for resume in resumes
    ]
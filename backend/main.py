# main.py - FastAPI backend for resume verification
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional, Dict, Union, Any,Annotated
from pydantic import BaseModel, Field
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Resume Verification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.resume_verification

# Pydantic models for data validation
class EducationSend(BaseModel):
    degree: str
    institution: str

class EducationActual(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None

class Education(BaseModel):
    send: EducationSend
    actual: EducationActual
    verified: bool

class WorkExperienceSend(BaseModel):
    position: str
    company: str

class WorkExperienceActual(BaseModel):
    position: Optional[str] = None
    company: Optional[str] = None

class WorkExperience(BaseModel):
    send: WorkExperienceSend
    actual: WorkExperienceActual
    verified: bool

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator):
        return {"type": "string"}

class Resume(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    resume_id: str
    job_id: str
    username: str
    is_verified: str
    status: str
    ranking_score: float
    name: str
    email: str
    phone: str
    education: List[Education]
    work_experience: List[WorkExperience]

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
class VerificationRequest(BaseModel):
    resume_id: str
    type: str  # "education" or "work"
    index: int
    action: str  # "confirm" or "reject"

# API endpoints

@app.get("/api/resumes", response_model=List[Resume])
async def get_resumes():
    """Get all resumes from the database"""
    resumes = await db.resumes.find().to_list(1000)
    return resumes

@app.get("/api/resumes/{resume_id}", response_model=Resume)
async def get_resume(resume_id: str):
    """Get a specific resume by ID"""
    resume = await db.resumes.find_one({"resume_id": resume_id})
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@app.post("/api/verify")
async def verify_qualification(verification: VerificationRequest):
    """Verify a qualification (education or work experience)"""
    # Check if the resume exists
    resume = await db.resumes.find_one({"resume_id": verification.resume_id})
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Determine the field path based on type
    if verification.type == "education":
        field_path = f"education.{verification.index}.verified"
        
        # Check if the index is valid
        if verification.index >= len(resume["education"]):
            raise HTTPException(status_code=400, detail="Education index out of range")
    
    elif verification.type == "work":
        field_path = f"work_experience.{verification.index}.verified"
        
        # Check if the index is valid
        if verification.index >= len(resume["work_experience"]):
            raise HTTPException(status_code=400, detail="Work experience index out of range")
    
    else:
        raise HTTPException(status_code=400, detail="Invalid qualification type")
    
    # Determine the verified status based on action
    verified = verification.action == "confirm"
    
    # Update the document
    result = await db.resumes.update_one(
        {"resume_id": verification.resume_id},
        {"$set": {field_path: verified}}
    )
    
    if result.modified_count == 0:
        return {"message": "No changes made"}
    
    # If all qualifications are verified, update the overall resume verification status
    if verified:
        updated_resume = await db.resumes.find_one({"resume_id": verification.resume_id})
        all_verified = True
        
        # Check education verifications
        for edu in updated_resume["education"]:
            if not edu["verified"]:
                all_verified = False
                break
        
        # If all education is verified, check work experience
        if all_verified:
            for work in updated_resume["work_experience"]:
                if not work["verified"]:
                    all_verified = False
                    break
        
        # If all qualifications are verified, update resume status
        if all_verified:
            await db.resumes.update_one(
                {"resume_id": verification.resume_id},
                {"$set": {"is_verified": "VERIFIED"}}
            )
    
    return {"success": True, "action": verification.action}

# Optional: Endpoint to simulate blockchain verification
@app.post("/api/blockchain-verify")
async def blockchain_verify(
    data: Dict[str, Any] = Body(...)
):
    """
    Simulate blockchain verification of resume qualifications
    This would actually interact with a blockchain in a real implementation
    """
    resume_id = data.get("resume_id")
    qualification_type = data.get("type")  # "education" or "work"
    index = data.get("index")
    
    if not all([resume_id, qualification_type, index is not None]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # In a real implementation, this would verify the data on the blockchain
    # For this example, we'll just update the database directly
    
    field_path = f"{qualification_type}.{index}.verified"
    
    result = await db.resumes.update_one(
        {"resume_id": resume_id},
        {"$set": {field_path: True}}
    )
    
    if result.modified_count == 0:
        return {"message": "No changes made or resume not found"}
    
    return {
        "success": True,
        "message": f"Qualification verified via blockchain",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
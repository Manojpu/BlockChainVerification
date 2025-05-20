from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any
from app.utils.helpers import convert_objectid

from app.models.schemas import (
    ResumeInitVerificationRequest,
    ResumeEducationVerificationRequest,
    ResumeWorkExperienceVerificationRequest,
    VerificationResponse
)

from app.services.verification import (
    ResumeVerificationService,
    VerificationState
)

router = APIRouter(
    prefix="/resume-verification",
    tags=["resume-verification"],
    responses={404: {"description": "Not found"}},
)

def get_resume_verification_service():
    service = ResumeVerificationService()
    try:
        yield service
    finally:
        service.close()

@router.post("/initialize", response_model=VerificationResponse)
async def initialize_verification(
    request: ResumeInitVerificationRequest,
    service: ResumeVerificationService = Depends(get_resume_verification_service)
):
    """
    Initialize verification record for a resume and automatically start verification.
    """
    try:
        success, message, data = service.initialize_verification(request.resume_id)
        
        # Convert any ObjectId to string before returning
        if data:
            data = convert_objectid(data)
            
        return {
            "success": success,
            "message": message,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing verification: {str(e)}")

@router.post("/check-education", response_model=VerificationResponse)
async def check_education_verification(
    request: ResumeEducationVerificationRequest,
    service: ResumeVerificationService = Depends(get_resume_verification_service)
):
    """
    Check education verification status or initiate verification process.
    """
    try:
        success, message, data = service.check_education_verification(
            request.resume_id,
            request.education_index
        )
        
        # Convert any ObjectId to string before returning
        if data:
            data = convert_objectid(data)
            
        return {
            "success": success,
            "message": message,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking education verification: {str(e)}")

@router.post("/verify-education", response_model=VerificationResponse)
async def verify_education(
    request: ResumeEducationVerificationRequest,
    approval: bool = Query(True, description="True for approval, False for rejection"),
    service: ResumeVerificationService = Depends(get_resume_verification_service)
):
    """
    Approve or reject education verification and store result in blockchain.
    """
    try:
        success, message, data = service.verify_education(
            request.resume_id,
            request.education_index,
            approval
        )
        
        # Convert any ObjectId to string before returning
        if data:
            data = convert_objectid(data)
            
        return {
            "success": success,
            "message": message,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying education: {str(e)}")

@router.post("/check-work-experience", response_model=VerificationResponse)
async def check_work_experience_verification(
    request: ResumeWorkExperienceVerificationRequest,
    service: ResumeVerificationService = Depends(get_resume_verification_service)
):
    """
    Check work experience verification status or initiate verification process.
    """
    try:
        success, message, data = service.check_work_experience_verification(
            request.resume_id,
            request.experience_index
        )
        
        # Convert any ObjectId to string before returning
        if data:
            data = convert_objectid(data)
            
        return {
            "success": success,
            "message": message,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking work experience verification: {str(e)}")

@router.post("/verify-work-experience", response_model=VerificationResponse)
async def verify_work_experience(
    request: ResumeWorkExperienceVerificationRequest,
    approval: bool = Query(True, description="True for approval, False for rejection"),
    service: ResumeVerificationService = Depends(get_resume_verification_service)
):
    """
    Approve or reject work experience verification and store result in blockchain.
    """
    try:
        success, message, data = service.verify_work_experience(
            request.resume_id,
            request.experience_index,
            approval
        )
        
        # Convert any ObjectId to string before returning
        if data:
            data = convert_objectid(data)
            
        return {
            "success": success,
            "message": message,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying work experience: {str(e)}")
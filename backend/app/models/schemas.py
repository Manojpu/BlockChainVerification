"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import IntEnum
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class VerificationType(IntEnum):
    """Verification types matching the smart contract."""
    GPA = 0
    EMPLOYMENT = 1
    DEGREE = 2
    CERTIFICATE = 3

class GPAVerificationRequest(BaseModel):
    """Request model for GPA verification."""
    name: str = Field(..., description="Full name of the student")
    university: str = Field(..., description="Name of the university")
    gpa: float = Field(..., description="GPA value to verify", ge=0.0, le=4.0)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Kalana De Alwis",
                "university": "NSBM Green University",
                "gpa": 3.73
            }
        }

class DegreeVerificationRequest(BaseModel):
    """Request model for degree verification."""
    name: str = Field(..., description="Full name of the student")
    university: str = Field(..., description="Name of the university")
    degree: str = Field(..., description="Degree name to verify")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Kalana De Alwis",
                "university": "NSBM Green University",
                "degree": "BSc in Software Engineering"
            }
        }

class EmploymentVerificationRequest(BaseModel):
    """Request model for employment verification."""
    name: str = Field(..., description="Full name of the employee")
    company: str = Field(..., description="Name of the company")
    job_title: Optional[str] = Field(None, description="Job title (optional)")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Shehani Jayawardena",
                "company": "99X Technology",
                "job_title": "ML Engineer" 
            }
        }

class VerificationResponse(BaseModel):
    """Response model for verification results."""
    data: Dict[str, Any] = Field(..., description="Original data that was verified")
    data_hash: str = Field(..., description="Hash of the data used for blockchain storage")
    is_verified: bool = Field(..., description="Verification result")
    verification_type: str = Field(..., description="Type of verification performed")
    details: str = Field(..., description="Details about the verification")
    timestamp: int = Field(..., description="Time when verification was performed")
    tx_hash: Optional[str] = Field(None, description="Transaction hash on blockchain")
    status: str = Field(..., description="Status of verification (new or existing)")
    
    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "name": "Kalana De Alwis",
                    "university": "NSBM Green University",
                    "gpa": 3.73
                },
                "data_hash": "0x8f2e3c5a2d4b6c8a0e1f3d5b7a9c2e4f6d8a0b2c4e6f8a0c2e4f6d8a0b2c4e6f8",
                "is_verified": True,
                "verification_type": "GPA",
                "details": "Verified GPA of 3.73 for Kalana De Alwis at NSBM Green University",
                "timestamp": 1651234567,
                "tx_hash": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
                "status": "new"
            }
        }

class BlockchainStatus(BaseModel):
    """Model for blockchain status information."""
    provider: str = Field(..., description="Blockchain provider URL")
    contract_address: str = Field(..., description="Verification contract address")
    block_number: int = Field(..., description="Current block number")
    verification_count: int = Field(..., description="Total number of verifications stored")
    
    class Config:
        schema_extra = {
            "example": {
                "provider": "http://localhost:7545",
                "contract_address": "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24",
                "block_number": 12345,
                "verification_count": 42
            }
        }

class VerificationListResponse(BaseModel):
    """Response model for listing verifications."""
    verifications: List[Dict[str, Any]] = Field(..., description="List of verification records")
    total: int = Field(..., description="Total number of verification records")
    
    class Config:
        schema_extra = {
            "example": {
                "verifications": [
                    {
                        "data_hash": "0x8f2e3c5a2d4b6c8a0e1f3d5b7a9c2e4f6d8a0b2c4e6f8a0c2e4f6d8a0b2c4e6f8",
                        "is_verified": True,
                        "verification_type": "GPA",
                        "details": "Verified GPA of 3.73 for Kalana De Alwis at NSBM Green University",
                        "timestamp": 1651234567,
                        "oracle_address": "0x1234567890abcdef1234567890abcdef12345678"
                    },
                    {
                        "data_hash": "0xa1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
                        "is_verified": True,
                        "verification_type": "EMPLOYMENT",
                        "details": "Verified Shehani Jayawardena worked at 99X Technology as ML Engineer",
                        "timestamp": 1651234568,
                        "oracle_address": "0x1234567890abcdef1234567890abcdef12345678"
                    }
                ],
                "total": 2
            }
        }

class VerificationState(str, Enum):
    """Enum for verification states of individual items."""
    PENDING = "PENDING"
    BLOCKCHAIN_VERIFIED = "BLOCKCHAIN_VERIFIED"
    SUBMITTED = "SUBMITTED" 
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class VerificationStatus(str, Enum):
    """Enum for overall verification status."""
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"



class ResumeEducationVerificationRequest(BaseModel):
    resume_id: str
    education_index: int

class ResumeWorkExperienceVerificationRequest(BaseModel):
    resume_id: str
    experience_index: int

class ResumeInitVerificationRequest(BaseModel):
    resume_id: str

class EducationData(BaseModel):
    degree: str
    institution: str

class WorkExperienceData(BaseModel):
    position: str
    company: str

class EducationVerification(BaseModel):
    send: EducationData
    actual: Optional[EducationData] = None
    verified: VerificationState = VerificationState.PENDING


class WorkExperienceVerification(BaseModel):
    send: WorkExperienceData
    actual: Optional[WorkExperienceData] = None
    verified: VerificationState = VerificationState.PENDING


class VerificationInfo(BaseModel):
    resume_id: str
    job_id: str
    username: str
    is_verified: VerificationStatus = VerificationStatus.PENDING
    status: str
    ranking_score: float
    name: str
    email: str
    phone: str
    education: List[EducationVerification]
    work_experience: List[WorkExperienceVerification]

class VerificationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Update the EducationData class
class EducationData(BaseModel):
    degree: str
    institution: str
    gpa: Optional[float] = None  # Add GPA field
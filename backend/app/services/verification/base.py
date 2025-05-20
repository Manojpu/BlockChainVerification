"""
Base verification service and common utilities.
"""
import logging
from typing import Dict, Any, Tuple, List, Optional
from bson.objectid import ObjectId

from app.services.mock_db import MockDatabase
from app.services.blockchain import BlockchainClient
from app.services.oracle_simulator import OracleSimulator, VerificationType
from app.utils.helpers import extract_gpa

from .common import VerificationState
from .status import VerificationStatusService
from .education import EducationVerificationService
from .work_experience import WorkExperienceVerificationService

logger = logging.getLogger(__name__)



class ResumeVerificationService:
    """Service for verifying resume data against blockchain and institutional databases."""
    
    def __init__(self):
        """Initialize the resume verification service."""
        self.db = MockDatabase()
        self.blockchain = BlockchainClient()
        self.oracle = OracleSimulator()
        self.status_service = VerificationStatusService(self.db)
        self.education_service = EducationVerificationService(self.db, self.blockchain, self.oracle)
        self.work_experience_service = WorkExperienceVerificationService(self.db, self.blockchain, self.oracle)
        logger.info("ResumeVerificationService initialized")
    
    def initialize_verification(self, resume_id: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Initialize verification record for a resume and automatically start verification.
        
        Args:
            resume_id: Resume ID to verify
            
        Returns:
            Tuple of (success, message, data)
        """
        # Get resume data
        resume = self.db.get_resume_by_id(resume_id)
        if not resume:
            return False, f"Resume with ID {resume_id} not found", {}
        
        # Check if verification already exists
        existing = self.db.get_verification_info(resume_id)
        if existing:
            return False, f"Verification for resume ID {resume_id} already exists", existing
        
        # Create verification record
        verification_data = {
            "resume_id": resume_id,
            "job_id": resume.get("job_id", ""),
            "username": resume.get("username", ""),
            "is_verified": "PENDING",  # Set to PENDING initially
            "status": resume.get("status", ""),
            "ranking_score": resume.get("ranking_score", 0),
            "name": resume.get("name", ""),
            "email": resume.get("email", ""),
            "phone": resume.get("phone", ""),
            "education": [],
            "work_experience": []
        }
        
        # Process education data
        for edu in resume.get("education", []):
            # Initialize education entry with basic fields
            edu_entry = {
                "send": {
                    "degree": edu.get("degree", ""),
                    "institution": edu.get("institution", "")
                },
                "actual": {
                    "degree": None,
                    "institution": None
                },
                "verified": VerificationState.PENDING  # Use enum string instead of boolean
            }
            
            # Check for GPA in details field
            details = edu.get("details", "")
            if details:
                gpa = extract_gpa(details)
                if gpa is not None:
                    # Only add GPA fields if we found a valid GPA
                    edu_entry["send"]["gpa"] = gpa
                    edu_entry["actual"]["gpa"] = None
                    logger.info(f"Extracted GPA {gpa} from details: '{details}'")
            
            verification_data["education"].append(edu_entry)
        
        # Process work experience data
        for exp in resume.get("work_experience", []):
            verification_data["work_experience"].append({
                "send": {
                    "position": exp.get("position", ""),
                    "company": exp.get("company", "")
                },
                "actual": {
                    "position": None,
                    "company": None
                },
                "verified": VerificationState.PENDING  # Use enum string instead of boolean
            })
        
        # Store verification record
        record_id = self.db.create_verification_record(verification_data)
        if not record_id:
            return False, "Failed to create verification record", {}
        
        # Get the created record
        created_record = self.db.get_verification_info(resume_id)
        
        # Now automatically start verification for all entries
        verification_results = []
        
        # Start education verification
        for i in range(len(verification_data["education"])):
            try:
                success, message, _ = self.check_education_verification(resume_id, i)
                verification_results.append(f"Education {i}: {message}")
            except Exception as e:
                verification_results.append(f"Education {i}: Error - {str(e)}")
        
        # Start work experience verification  
        for i in range(len(verification_data["work_experience"])):
            try:
                success, message, _ = self.check_work_experience_verification(resume_id, i)
                verification_results.append(f"Work Experience {i}: {message}")
            except Exception as e:
                verification_results.append(f"Work Experience {i}: Error - {str(e)}")
        
        # Get the updated record after verifications
        updated_record = self.db.get_verification_info(resume_id)
        
        return True, f"Verification record created and verification started: {'; '.join(verification_results)}", updated_record
    
    def check_education_verification(self, resume_id: str, education_index: int) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check education verification against blockchain or perform verification.
        
        Args:
            resume_id: Resume ID
            education_index: Index of education to verify
            
        Returns:
            Tuple of (success, message, data)
        """
        return self.education_service.check_verification(resume_id, education_index)
    
    def verify_education(self, resume_id: str, education_index: int, approval: bool = True) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verify education data against mock databases and store in blockchain.
        This function is called when an admin manually approves or rejects an education verification.
        
        Args:
            resume_id: Resume ID
            education_index: Index of education to verify
            approval: Whether the admin approves (True) or rejects (False) the verification
            
        Returns:
            Tuple of (success, message, data)
        """
        return self.education_service.verify(resume_id, education_index, approval)
    
    def check_work_experience_verification(self, resume_id: str, experience_index: int) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check work experience verification against blockchain or perform verification.
        
        Args:
            resume_id: Resume ID
            experience_index: Index of work experience to verify
            
        Returns:
            Tuple of (success, message, data)
        """
        return self.work_experience_service.check_verification(resume_id, experience_index)
    
    def verify_work_experience(self, resume_id: str, experience_index: int, approval: bool = True) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verify work experience data against mock databases and store in blockchain.
        This is called when admin clicks the "confirm" or "reject" button.
        
        Args:
            resume_id: Resume ID
            experience_index: Index of work experience to verify
            approval: Whether the admin approves (True) or rejects (False) the verification
            
        Returns:
            Tuple of (success, message, data)
        """
        return self.work_experience_service.verify(resume_id, experience_index, approval)
    
    def close(self):
        """Close connections."""
        self.db.close()
        logger.info("ResumeVerificationService connections closed")
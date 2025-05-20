"""
Verification status management service.
"""
import logging
from typing import Dict, Any

from app.services.mock_db import MockDatabase
from .common import VerificationState

logger = logging.getLogger(__name__)

class VerificationStatusService:
    """Service for managing overall verification status."""
    
    def __init__(self, db: MockDatabase):
        """Initialize the verification status service."""
        self.db = db
        logger.info("VerificationStatusService initialized")
    
    def update_overall_verification_status(self, verification: Dict[str, Any]) -> bool:
        """
        Update the overall verification status based on individual verifications.
        Calculate percentage of verified items and set overall status accordingly.
        
        Args:
            verification: Verification record
            
        Returns:
            True if all verifications are complete, False otherwise
        """
        # First check if all items have been processed (not in PENDING state)
        all_edu_processed = all(edu["verified"] != VerificationState.PENDING for edu in verification["education"]) if verification["education"] else True
        all_exp_processed = all(exp["verified"] != VerificationState.PENDING for exp in verification["work_experience"]) if verification["work_experience"] else True
        
        # If not all processed, keep status as PENDING
        if not (all_edu_processed and all_exp_processed):
            verification["is_verified"] = "PENDING"
            self.db.update_verification_record(str(verification["_id"]), {"is_verified": "PENDING"})
            logger.info(f"Some verifications still pending, keeping status as PENDING for record {verification['_id']}")
            return False
        
        # Count verified items
        total_items = len(verification["education"]) + len(verification["work_experience"])
        verified_count = 0
        
        # Count education verifications
        for edu in verification["education"]:
            if edu["verified"] == VerificationState.VERIFIED or edu["verified"] == VerificationState.BLOCKCHAIN_VERIFIED:
                verified_count += 1
        
        # Count work experience verifications
        for exp in verification["work_experience"]:
            if exp["verified"] == VerificationState.VERIFIED or exp["verified"] == VerificationState.BLOCKCHAIN_VERIFIED:
                verified_count += 1
        
        # Calculate percentage
        verification_percentage = (verified_count / total_items * 100) if total_items > 0 else 0
        logger.info(f"Verification percentage: {verification_percentage}% ({verified_count}/{total_items})")
        
        # Update overall status based on threshold (75%)
        if verification_percentage >= 75:
            verification["is_verified"] = "VERIFIED"
            self.db.update_verification_record(str(verification["_id"]), {"is_verified": "VERIFIED"})
            logger.info(f"Verification percentage {verification_percentage}% meets threshold, setting status to VERIFIED")
            return True
        else:
            verification["is_verified"] = "REJECTED"
            self.db.update_verification_record(str(verification["_id"]), {"is_verified": "REJECTED"})
            logger.info(f"Verification percentage {verification_percentage}% below threshold, setting status to REJECTED")
            return False
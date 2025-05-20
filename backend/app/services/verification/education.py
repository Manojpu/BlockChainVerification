"""
Education verification service.
"""
import logging
from typing import Dict, Any, Tuple, Optional

from app.services.mock_db import MockDatabase
from app.services.blockchain import BlockchainClient
from app.services.oracle_simulator import OracleSimulator, VerificationType
from .status import VerificationStatusService
from .common import VerificationState

logger = logging.getLogger(__name__)

class EducationVerificationService:
    """Service for verifying education data against blockchain and institutional databases."""
    
    def __init__(self, db: MockDatabase, blockchain: BlockchainClient, oracle: OracleSimulator):
        """Initialize the education verification service."""
        self.db = db
        self.blockchain = blockchain
        self.oracle = oracle
        self.status_service = VerificationStatusService(db)
        logger.info("EducationVerificationService initialized")
    
    def check_verification(self, resume_id: str, education_index: int) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check education verification against blockchain or perform verification.
        
        Args:
            resume_id: Resume ID
            education_index: Index of education to verify
            
        Returns:
            Tuple of (success, message, data)
        """
        logger.info(f"Starting education verification for resume {resume_id}, education index {education_index}")
        # Get verification record
        verification = self.db.get_verification_info(resume_id)
        if not verification:
            return False, f"Verification record for resume ID {resume_id} not found", {}
        
        # Check if education index is valid
        if education_index >= len(verification.get("education", [])):
            return False, f"Education index {education_index} is out of range", {}
        
        # Get education data
        education = verification["education"][education_index]
        if education["verified"] in [VerificationState.VERIFIED, VerificationState.REJECTED]:
            return True, f"Education already in final state: {education['verified']}", verification
        
        # Prepare data for blockchain verification
        degree = education["send"]["degree"]
        institution = education["send"]["institution"]
        name = verification["name"]
        
        verification_data = {
            "name": name,
            "university": institution,
            "degree": degree
        }

        gpa = education["send"].get("gpa")
        if gpa is not None:
            verification_data["gpa"] = gpa
        
        # Create hash and check if already verified on blockchain
        data_hash = self.blockchain.create_data_hash(verification_data)
        exists = self.blockchain.verification_exists(data_hash)
        
        if exists:
            # Get verification status from blockchain
            logger.info(f"Verification data found on blockchain: {verification_data}")
            logger.info(f"Data hash: {data_hash}")
            blockchain_status = self.blockchain.get_verification_status(data_hash)
            is_verified = blockchain_status["is_verified"] if isinstance(blockchain_status, dict) else blockchain_status[0]
            
            # Update verification record
            education["verified"] = VerificationState.BLOCKCHAIN_VERIFIED  # Mark as blockchain verified
            if is_verified:
                education["actual"]["degree"] = degree
                education["actual"]["institution"] = institution
                if gpa is not None:
                    education["actual"]["gpa"] = gpa
            
            # Update the record
            update_data = {
                f"education.{education_index}": education
            }
            
            # Update database
            self.db.update_verification_record(str(verification["_id"]), update_data)
            
            # Check if all verifications are complete
            self.status_service.update_overall_verification_status(verification)
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "Education verification status retrieved from blockchain", updated_record
        
        # Not in blockchain, query mock database - FIXED QUERY STRUCTURE
        query_params = {
            "full_name": name,
            "university": institution
            # Note: We'll do the institution comparison after fetching the record
            # since the formats might be slightly different
        }
        
        # Query the university records
        university_record = self.db.university_collection.find_one(query_params)
        
        if university_record:
            # Record found, check if degree and institution match
            db_degree = university_record.get("degree", "")
            db_institution = university_record.get("university", "")  # Using university field from DB
            db_gpa = university_record.get("gpa")

            logger.info(f"Found university record: {university_record}")
            logger.info(f"Comparing: DB degree '{db_degree}' with claimed '{degree}'")
            logger.info(f"Comparing: DB institution '{db_institution}' with claimed '{institution}'")
            
            # Update verification data with actual values from database
            education["actual"]["degree"] = db_degree
            education["actual"]["institution"] = db_institution
            if db_gpa is not None:
                education["actual"]["gpa"] = db_gpa
            
            # Set status as SUBMITTED (waiting for admin confirmation)
            education["verified"] = VerificationState.SUBMITTED
            
            # Update the record
            update_data = {
                f"education.{education_index}": education
            }
            
            # Update database and set overall status to PENDING
            self.db.update_verification_record(str(verification["_id"]), update_data)
            self.db.update_verification_record(str(verification["_id"]), {"is_verified": "PENDING"})
            
            # Check if all verifications are complete
            self.status_service.update_overall_verification_status(verification)
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "Education information found in database. Awaiting verification.", updated_record
        else:
            # No record found, set to PENDING for manual verification
            education["verified"] = VerificationState.PENDING
            update_data = {
                f"education.{education_index}": education
            }
            self.db.update_verification_record(str(verification["_id"]), update_data)
            self.db.update_verification_record(str(verification["_id"]), {"is_verified": "PENDING"})
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "No matching education records found. Awaiting manual verification.", updated_record
    
    def verify(self, resume_id: str, education_index: int, approval: bool = True) -> Tuple[bool, str, Dict[str, Any]]:
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
        # Get verification record
        verification = self.db.get_verification_info(resume_id)
        if not verification:
            return False, f"Verification record for resume ID {resume_id} not found", {}
        
        # Check if education index is valid
        if education_index >= len(verification.get("education", [])):
            return False, f"Education index {education_index} is out of range", {}
        
        # Get education data
        education = verification["education"][education_index]
        
        # If rejecting, mark as rejected and don't store on blockchain
        if not approval:
            education["verified"] = VerificationState.REJECTED
            update_data = {
                f"education.{education_index}": education
            }
            self.db.update_verification_record(str(verification["_id"]), update_data)
            
            # Check if all verifications are complete and update overall status
            self.status_service.update_overall_verification_status(verification)
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "Education verification rejected", updated_record
        
        # Proceeding with approval
        degree = education["send"]["degree"]
        institution = education["send"]["institution"]
        name = verification["name"]
        
        # Prepare data for blockchain verification
        verification_data = {
            "name": name,
            "university": institution,
            "degree": degree
        }

        gpa = education["send"].get("gpa")
        if gpa is not None:
            verification_data["gpa"] = gpa
        
        # Check if already in blockchain
        data_hash = self.blockchain.create_data_hash(verification_data)
        exists = self.blockchain.verification_exists(data_hash)
        
        if exists:
            # Already verified in blockchain, just update our records
            blockchain_status = self.blockchain.get_verification_status(data_hash)
            is_verified = blockchain_status["is_verified"] if isinstance(blockchain_status, dict) else blockchain_status[0]
            logger.info(f"Verification status from blockchain: {blockchain_status}")
            
            if is_verified:
                # Update verification record with actual values and set as verified
                education["verified"] = VerificationState.VERIFIED
                education["actual"]["degree"] = degree
                education["actual"]["institution"] = institution
                if gpa is not None and not education["actual"].get("gpa"):
                    education["actual"]["gpa"] = gpa
                
                # Update the record in database
                update_data = {f"education.{education_index}": education}
                self.db.update_verification_record(str(verification["_id"]), update_data)
                
                # Check if all verifications are complete and update overall status
                self.status_service.update_overall_verification_status(verification)
                
                updated_record = self.db.get_verification_info(resume_id)
                return True, "Education already verified in blockchain", updated_record
        
        # Store verification on blockchain (this is the manual verification by admin)
        logger.info(f"Storing education verification on blockchain for {name}, {degree} at {institution}")
        
        # Set the verification to verified
        education["verified"] = VerificationState.VERIFIED
        
        # If actual values weren't set during the check phase, use the send values
        if not education["actual"]["degree"]:
            education["actual"]["degree"] = degree
        if not education["actual"]["institution"]:
            education["actual"]["institution"] = institution
        if gpa is not None and not education["actual"].get("gpa"):
            education["actual"]["gpa"] = gpa

        # Store on blockchain using oracle
        result = self.oracle.verify_and_store_on_blockchain(
            verification_data,
            VerificationType.DEGREE
        )
        
        # Update the record
        update_data = {
            f"education.{education_index}": education
        }
        self.db.update_verification_record(str(verification["_id"]), update_data)
        
        # Check if all verifications are complete and update overall status
        self.status_service.update_overall_verification_status(verification)
        
        # Get updated record
        updated_record = self.db.get_verification_info(resume_id)
        return True, "Education verification completed and stored on blockchain", updated_record
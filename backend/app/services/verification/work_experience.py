"""
Work experience verification service.
"""
import logging
from typing import Dict, Any, Tuple, Optional, List

from app.services.mock_db import MockDatabase
from app.services.blockchain import BlockchainClient
from app.services.oracle_simulator import OracleSimulator, VerificationType
from .status import VerificationStatusService
from .common import VerificationState

logger = logging.getLogger(__name__)

class WorkExperienceVerificationService:
    """Service for verifying work experience data against blockchain and company databases."""
    
    def __init__(self, db: MockDatabase, blockchain: BlockchainClient, oracle: OracleSimulator):
        """Initialize the work experience verification service."""
        self.db = db
        self.blockchain = blockchain
        self.oracle = oracle
        self.status_service = VerificationStatusService(db)
        logger.info("WorkExperienceVerificationService initialized")
    
    def check_verification(self, resume_id: str, experience_index: int) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check work experience verification against blockchain or perform verification.
        
        Args:
            resume_id: Resume ID
            experience_index: Index of work experience to verify
            
        Returns:
            Tuple of (success, message, data)
        """
        logger.info(f"Starting work experience verification for resume {resume_id}, experience index {experience_index}")
        # Get verification record
        verification = self.db.get_verification_info(resume_id)
        if not verification:
            return False, f"Verification record for resume ID {resume_id} not found", {}
        
        # Check if experience index is valid
        if experience_index >= len(verification.get("work_experience", [])):
            return False, f"Experience index {experience_index} is out of range", {}
        
        # Get work experience data
        experience = verification["work_experience"][experience_index]
        if experience["verified"] in [VerificationState.VERIFIED, VerificationState.REJECTED]:
            return True, f"Work experience already in final state: {experience['verified']}", verification
        
        # Prepare data for blockchain verification
        position = experience["send"]["position"]
        company = experience["send"]["company"]
        name = verification["name"]
        
        verification_data = {
            "name": name,
            "company": company,
            "job_title": position
        }
        
        # Create hash and check if already verified on blockchain
        data_hash = self.blockchain.create_data_hash(verification_data)
        exists = self.blockchain.verification_exists(data_hash)
        
        if exists:
            # Get verification status from blockchain
            logger.info(f"Work experience verification data found on blockchain: {verification_data}")
            logger.info(f"Data hash: {data_hash}")
            blockchain_status = self.blockchain.get_verification_status(data_hash)
            is_verified = blockchain_status["is_verified"] if isinstance(blockchain_status, dict) else blockchain_status[0]
            
            # Update verification record
            experience["verified"] = VerificationState.BLOCKCHAIN_VERIFIED
            if is_verified:
                experience["actual"]["position"] = position
                experience["actual"]["company"] = company
            
            # Update the record
            update_data = {
                f"work_experience.{experience_index}": experience
            }
            
            # Update database
            result = self.db.update_verification_record(str(verification["_id"]), update_data)
            logger.info(f"Updated verification record from blockchain: {result}")
            
            # Check if all verifications are complete
            self.status_service.update_overall_verification_status(verification)
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "Work experience verification status retrieved from blockchain", updated_record
        
        # Not in blockchain, try direct query first
        logger.info(f"Querying employment records for {name} at {company}")
        
        # Try simple direct query first
        direct_query = {"full_name": name, "company": company}
        employment_records = self.db.company_collection.find(direct_query)
        records_list = list(employment_records)
        
        # If no records found with direct query, try case insensitive
        if not records_list:
            logger.info("No exact match found, trying case insensitive search")
            case_insensitive_query = {
                "full_name": {"$regex": name, "$options": "i"},
                "company": {"$regex": company, "$options": "i"}
            }
            employment_records = self.db.company_collection.find(case_insensitive_query)
            records_list = list(employment_records)
        
        # If still no records, try partial match
        if not records_list:
            logger.info("No case-insensitive match found, trying partial match")
            partial_match_query = {
                "full_name": {"$regex": name, "$options": "i"},
                "company": {"$regex": ".*" + company + ".*", "$options": "i"}
            }
            employment_records = self.db.company_collection.find(partial_match_query)
            records_list = list(employment_records)
        
        if records_list:
            logger.info(f"Found {len(records_list)} employment records")
            
            # Look for position match
            matched_record = None
            for record in records_list:
                record_position = record.get("position", "")
                if position.lower() in record_position.lower() or record_position.lower() in position.lower():
                    matched_record = record
                    logger.info(f"Found matching position: {record_position}")
                    break
            
            # Use the first record if no position match
            if not matched_record and records_list:
                matched_record = records_list[0]
                logger.info(f"Using first record as no exact position match found")
            
            if matched_record:
                # Update verification data with actual values
                record_position = matched_record.get("position", "")
                record_company = matched_record.get("company", "")
                
                logger.info(f"Updating actual values - Position: {record_position}, Company: {record_company}")
                
                experience["actual"]["position"] = record_position
                experience["actual"]["company"] = record_company
                
                # Set as SUBMITTED (waiting for admin confirmation)
                experience["verified"] = VerificationState.SUBMITTED
                
                # Update the record
                update_data = {
                    f"work_experience.{experience_index}": experience
                }
                
                # Update the database record
                result = self.db.update_verification_record(str(verification["_id"]), update_data)
                logger.info(f"Updated work experience data: {result}")
                
                # Set overall status to PENDING
                pending_result = self.db.update_verification_record(str(verification["_id"]), {"is_verified": "PENDING"})
                logger.info(f"Set overall status to PENDING: {pending_result}")
                
                updated_record = self.db.get_verification_info(resume_id)
                return True, "Work experience information fetched. Awaiting verification.", updated_record
        
        # No matching records found
        logger.info(f"No matching employment records found for {name} at {company}")
        
        # Set to PENDING for manual verification
        experience["verified"] = VerificationState.PENDING
        update_data = {
            f"work_experience.{experience_index}": experience
        }
        self.db.update_verification_record(str(verification["_id"]), update_data)
        pending_result = self.db.update_verification_record(str(verification["_id"]), {"is_verified": "PENDING"})
        logger.info(f"Set status to PENDING: {pending_result}")
        
        updated_record = self.db.get_verification_info(resume_id)
        return True, "No matching employment records found. Awaiting manual verification.", updated_record
    
    def verify(self, resume_id: str, experience_index: int, approval: bool = True) -> Tuple[bool, str, Dict[str, Any]]:
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
        logger.info(f"Admin {'approving' if approval else 'rejecting'} work experience verification for resume {resume_id}, experience index {experience_index}")
        
        # Get verification record
        verification = self.db.get_verification_info(resume_id)
        if not verification:
            return False, f"Verification record for resume ID {resume_id} not found", {}
        
        # Check if experience index is valid
        if experience_index >= len(verification.get("work_experience", [])):
            return False, f"Experience index {experience_index} is out of range", {}
        
        # Get work experience data
        experience = verification["work_experience"][experience_index]
        
        # If rejecting, mark as rejected and don't store on blockchain
        if not approval:
            experience["verified"] = VerificationState.REJECTED
            update_data = {
                f"work_experience.{experience_index}": experience
            }
            self.db.update_verification_record(str(verification["_id"]), update_data)
            
            # Check if all verifications are complete and update overall status
            self.status_service.update_overall_verification_status(verification)
            
            updated_record = self.db.get_verification_info(resume_id)
            return True, "Work experience verification rejected", updated_record
        
        # Proceeding with approval
        position = experience["send"]["position"]
        company = experience["send"]["company"]
        name = verification["name"]
        
        # Prepare data for blockchain verification
        verification_data = {
            "name": name,
            "company": company,
            "job_title": position
        }
        
        # Check if already in blockchain
        data_hash = self.blockchain.create_data_hash(verification_data)
        exists = self.blockchain.verification_exists(data_hash)
        
        if exists:
            # Already verified in blockchain, just update our records
            blockchain_status = self.blockchain.get_verification_status(data_hash)
            is_verified = blockchain_status["is_verified"] if isinstance(blockchain_status, dict) else blockchain_status[0]
            
            if is_verified:
                # Update verification record with actual values and set as verified
                experience["verified"] = VerificationState.VERIFIED
                experience["actual"]["position"] = position
                experience["actual"]["company"] = company
                
                # Update the record in database
                update_data = {f"work_experience.{experience_index}": experience}
                self.db.update_verification_record(str(verification["_id"]), update_data)
                
                # Check if all verifications are complete and update overall status
                self.status_service.update_overall_verification_status(verification)
                
                updated_record = self.db.get_verification_info(resume_id)
                return True, "Work experience already verified in blockchain", updated_record
        
        # Store verification on blockchain (this is the manual verification by admin)
        logger.info(f"Storing work experience verification on blockchain for {name}, {position} at {company}")
        
        # Set the verification to verified
        experience["verified"] = VerificationState.VERIFIED
        
        # If actual values weren't set during the check phase, use the send values
        if not experience["actual"]["position"]:
            experience["actual"]["position"] = position
        if not experience["actual"]["company"]:
            experience["actual"]["company"] = company
        
        # Store on blockchain using oracle
        result = self.oracle.verify_and_store_on_blockchain(
            verification_data,
            VerificationType.EMPLOYMENT
        )
        
        # Update the record
        update_data = {
            f"work_experience.{experience_index}": experience
        }
        self.db.update_verification_record(str(verification["_id"]), update_data)
        
        # Check if all verifications are complete and update overall status
        self.status_service.update_overall_verification_status(verification)
        
        # Get updated record
        updated_record = self.db.get_verification_info(resume_id)
        return True, "Work experience verification completed and stored on blockchain", updated_record
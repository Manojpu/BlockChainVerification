# First, add the import for Enum
import logging
from enum import Enum
from typing import Dict, Any, Tuple, List, Optional
from bson.objectid import ObjectId

from app.services.mock_db import MockDatabase
from app.services.blockchain import BlockchainClient
from app.services.oracle_simulator import OracleSimulator, VerificationType
from app.utils.helpers import extract_gpa

logger = logging.getLogger(__name__)

# Add an enum for verification states
class VerificationState(str, Enum):
    PENDING = "PENDING"
    BLOCKCHAIN_VERIFIED = "BLOCKCHAIN_VERIFIED"
    SUBMITTED = "SUBMITTED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class ResumeVerificationService:
    """Service for verifying resume data against blockchain and institutional databases."""
    
    def __init__(self):
        """Initialize the resume verification service."""
        self.db = MockDatabase()
        self.blockchain = BlockchainClient()
        self.oracle = OracleSimulator()
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
            self._update_overall_verification_status(verification)
            
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
            self._update_overall_verification_status(verification)
            
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
            self._update_overall_verification_status(verification)
            
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
                self._update_overall_verification_status(verification)
                
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
        self._update_overall_verification_status(verification)
        
        # Get updated record
        updated_record = self.db.get_verification_info(resume_id)
        return True, "Education verification completed and stored on blockchain", updated_record
    
    def check_work_experience_verification(self, resume_id: str, experience_index: int) -> Tuple[bool, str, Dict[str, Any]]:
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
            self._update_overall_verification_status(verification)
            
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
            self._update_overall_verification_status(verification)
            
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
                self._update_overall_verification_status(verification)
                
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
        self._update_overall_verification_status(verification)
        
        # Get updated record
        updated_record = self.db.get_verification_info(resume_id)
        return True, "Work experience verification completed and stored on blockchain", updated_record
    
    def _update_overall_verification_status(self, verification: Dict[str, Any]) -> bool:
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
    
    def close(self):
        """Close connections."""
        self.db.close()
        logger.info("ResumeVerificationService connections closed")
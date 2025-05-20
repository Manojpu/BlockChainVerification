import json
import os
from typing import Dict, List, Any, Optional
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class MockDatabase:
    """
    Mock database class that simulates fetching data from university and company records.
    In a production environment, this would connect to actual institutional databases.
    """
    
    def __init__(self):
        """Initialize the mock database by loading JSON files."""
        # Connect to MongoDB for mock verification data
        self.mock_uri = os.getenv("MONGO_URI")
        self.mock_client = MongoClient(self.mock_uri)
        
        # Connect to MongoDB for resume rover data
        self.resume_uri = os.getenv("MONGO")
        self.resume_client = MongoClient(self.resume_uri)
        
        # Existing mock databases (using MONGO_URI)
        self.mock_db_u = self.mock_client["university_db"]
        self.mock_db_c = self.mock_client["company_db"]
        self.university_collection = self.mock_db_u["university_records"]
        self.company_collection = self.mock_db_c["employment_records"]
        
        # Resume rover database (using MONGO)
        self.resume_rover_db = self.resume_client["resume_rover_db"]
        self.parsed_resumes = self.resume_rover_db["parsed_resumes"]
        self.verification_info = self.resume_rover_db["verification_info"]
        
        # Load data from JSON files if collections are empty
        self._load_mock_data_if_empty()
        
        logger.info("MockDatabase initialized")
    
    def _load_mock_data_if_empty(self):
        """Load mock data from JSON files if collections are empty."""
        # Load university records
        if self.university_collection.count_documents({}) == 0:
            try:
                with open("data/university_records.json", "r") as file:
                    university_records = json.load(file)
                    if university_records:
                        self.university_collection.insert_many(university_records)
                        logger.info(f"Loaded {len(university_records)} university records")
            except Exception as e:
                logger.error(f"Error loading university records: {e}")
        
        # Load company records
        if self.company_collection.count_documents({}) == 0:
            try:
                with open("data/company_records.json", "r") as file:
                    company_records = json.load(file)
                    if company_records:
                        self.company_collection.insert_many(company_records)
                        logger.info(f"Loaded {len(company_records)} company records")
            except Exception as e:
                logger.error(f"Error loading company records: {e}")
    
    def get_university_record_by_params(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get university record based on query parameters.
        
        Args:
            params: Query parameters for filtering
                
        Returns:
            Matching record or None
        """
        # Case-insensitive search for name and university
        query = {}
        if "name" in params:
            query["full_name"] = {"$regex": f"^{params['name']}$", "$options": "i"}
        elif "full_name" in params:
            query["full_name"] = {"$regex": f"^{params['full_name']}$", "$options": "i"}
        
        if "university" in params:
            query["university"] = {"$regex": f"{params['university']}", "$options": "i"}
                
        logger.info(f"Querying university records with: {query}")
        return self.university_collection.find_one(query)
    
    def get_employment_record_by_params(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get employment records based on query parameters.
        
        Args:
            params: Query parameters for filtering
            
        Returns:
            List of matching records
        """
        # Build query - avoid nested regex structures that cause issues
        query = {}
        
        # Handle name field
        if "name" in params:
            query["full_name"] = {"$regex": f"{params['name']}", "$options": "i"}
        elif "full_name" in params and isinstance(params["full_name"], str):
            query["full_name"] = {"$regex": f"{params['full_name']}", "$options": "i"}
        elif "full_name" in params and isinstance(params["full_name"], dict):
            query["full_name"] = params["full_name"]
        
        # Handle company field
        if "company" in params and isinstance(params["company"], str):
            query["company"] = {"$regex": f"{params['company']}", "$options": "i"}
        elif "company" in params and isinstance(params["company"], dict):
            query["company"] = params["company"]
        
        # Handle job title/position field
        if "job_title" in params and params["job_title"]:
            # Try both position and job_title fields
            position_query = {"$or": [
                {"position": {"$regex": f"{params['job_title']}", "$options": "i"}},
                {"job_title": {"$regex": f"{params['job_title']}", "$options": "i"}}
            ]}
            query = {**query, **position_query}
        
        logger.info(f"Querying employment records with: {query}")
        return list(self.company_collection.find(query))
    
    def get_resume_by_id(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get parsed resume by ID.
        
        Args:
            resume_id: Resume ID
            
        Returns:
            Resume data or None
        """
        from bson.objectid import ObjectId
        
        try:
            object_id = ObjectId(resume_id)
            resume = self.parsed_resumes.find_one({"_id": object_id})
            logger.info(f"Retrieved resume with ID: {resume_id}")
            return resume
        except Exception as e:
            logger.error(f"Error retrieving resume with ID {resume_id}: {e}")
            return None
    
    def get_verification_info(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get verification info by resume ID.
        
        Args:
            resume_id: Resume ID
            
        Returns:
            Verification info or None
        """
        from bson.objectid import ObjectId
        
        try:
            object_id = ObjectId(resume_id)
            verification = self.verification_info.find_one({"resume_id": resume_id})
            logger.info(f"Retrieved verification info for resume ID: {resume_id}")
            return verification
        except Exception as e:
            logger.error(f"Error retrieving verification info for resume ID {resume_id}: {e}")
            return None
    
    def create_verification_record(self, verification_data: Dict[str, Any]) -> str:
        """
        Create verification record.
        
        Args:
            verification_data: Verification data to store
            
        Returns:
            ID of created record
        """
        try:
            result = self.verification_info.insert_one(verification_data)
            logger.info(f"Created verification record with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating verification record: {e}")
            return None
    
    def update_verification_record(self, record_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update verification record.
        
        Args:
            record_id: Record ID
            update_data: Data to update
            
        Returns:
            Success status
        """
        from bson.objectid import ObjectId
        
        try:
            object_id = ObjectId(record_id)
            result = self.verification_info.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            success = result.modified_count > 0
            logger.info(f"Updated verification record {record_id}: {success}")
            return success
        except Exception as e:
            logger.error(f"Error updating verification record {record_id}: {e}")
            return False
    
    def close(self):
        """Close database connections."""
        if hasattr(self, 'mock_client') and self.mock_client:
            self.mock_client.close()
            logger.info("Closed mock database connections")
            
        if hasattr(self, 'resume_client') and self.resume_client:
            self.resume_client.close()
            logger.info("Closed resume database connections")
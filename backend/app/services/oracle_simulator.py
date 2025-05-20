"""
Oracle simulator to mimic Chainlink oracle behavior for data verification.
"""
import json
import time
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from enum import IntEnum
import sys
import os

# Fix imports to work both as module and when run directly
try:
    # Try relative import first (when imported as module)
    from .mock_db import MockDatabase
    from .blockchain import BlockchainClient, VerificationType
except ImportError:
    # Fall back to absolute import (when run as script)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from app.services.mock_db import MockDatabase
    from app.services.blockchain import BlockchainClient, VerificationType

class OracleSimulator:
    """
    Simulates Chainlink Oracle behavior to verify applicant information.
    """
    
    def __init__(self):
        """Initialize oracle with database and blockchain connections."""
        self.db = MockDatabase()
        self.blockchain = BlockchainClient()
        
    def verify_gpa(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify GPA information against mock university database.
        
        Args:
            data: Dictionary containing name, university, and gpa to verify
            
        Returns:
            Tuple of (verification_result, details)
        """
        # Extract required fields
        name = data.get("name")
        university = data.get("university")
        claimed_gpa = data.get("gpa")
        
        if not all([name, university, claimed_gpa]):
            return False, "Missing required fields (name, university, gpa)"
        
        # Query mock database
        query_params = {"name": name, "university": university}
        record = self.db.get_university_record_by_params(query_params)
        
        if not record:
            return False, f"No records found for {name} at {university}"
        
        # Compare claimed GPA with database record
        actual_gpa = record.get("gpa")
        
        # Determine if they match (within small floating point error)
        if abs(float(claimed_gpa) - float(actual_gpa)) < 0.01:
            return True, f"Verified GPA of {actual_gpa} for {name} at {university}"
        else:
            return False, f"GPA mismatch for {name} at {university}. Claimed: {claimed_gpa}, Actual: {actual_gpa}"
    
    def verify_degree(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify degree information against mock university database.
        
        Args:
            data: Dictionary containing name, university, and degree to verify
            
        Returns:
            Tuple of (verification_result, details)
        """
        # Extract required fields
        name = data.get("name")
        university = data.get("university")
        claimed_degree = data.get("degree")
        
        if not all([name, university, claimed_degree]):
            return False, "Missing required fields (name, university, degree)"
        
        # Query mock database
        query_params = {"name": name, "university": university}
        record = self.db.get_university_record_by_params(query_params)
        
        if not record:
            return False, f"No records found for {name} at {university}"
        
        # Compare claimed degree with database record
        actual_degree = record.get("degree")
        
        # Determine if they match
        if claimed_degree.lower() == actual_degree.lower():
            return True, f"Verified {actual_degree} degree for {name} at {university}"
        else:
            return False, f"Degree mismatch for {name} at {university}. Claimed: {claimed_degree}, Actual: {actual_degree}"
    
    def verify_employment(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify employment information against mock company database.
        
        Args:
            data: Dictionary containing name, company, and job_title information
            
        Returns:
            Tuple of (verification_result, details)
        """
        # Extract required fields
        name = data.get("name")
        company = data.get("company")
        claimed_job_title = data.get("job_title", None)
        
        if not all([name, company]):
            return False, "Missing required fields (name, company)"
        
        # Query mock database
        query_params = {"name": name, "company": company}
        if claimed_job_title:
            query_params["job_title"] = claimed_job_title
            
        records = self.db.get_employment_record_by_params(query_params)
        
        if not records:
            return False, f"No employment records found for {name} at {company}"
        
        # If we found matching records, verification successful
        if claimed_job_title:
            return True, f"Verified {name} worked at {company} as {claimed_job_title}"
        else:
            job_titles = [r.get("job_title") for r in records]
            return True, f"Verified {name} worked at {company} as: {', '.join(job_titles)}"
    
    def verify_and_store_on_blockchain(self, 
                                      data: Dict[str, Any], 
                                      verification_type: VerificationType) -> Dict[str, Any]:
        """
        Verify the data against mock databases and store the result on blockchain.
        
        Args:
            data: Dictionary with data to verify
            verification_type: Type of verification to perform
            
        Returns:
            Dictionary with verification results and transaction details
        """
        # Create hash from data
        data_hash = self.blockchain.create_data_hash(data)
        print(f"Generated data hash: {data_hash}")
        
        # Check if verification already exists on blockchain
        exists = self.blockchain.verification_exists(data_hash)
        print(f"Verification exists: {exists}")
        
        if exists:
            # Get existing verification
            verification = self.blockchain.get_verification_status(data_hash)
            verification["data_hash"] = data_hash
            verification["status"] = "existing"
            verification["data"] = data
            return verification
        
        # Perform verification based on type
        print(f"Performing verification of type: {verification_type.name}")
        if verification_type == VerificationType.GPA:
            is_verified, details = self.verify_gpa(data)
        elif verification_type == VerificationType.DEGREE:
            is_verified, details = self.verify_degree(data)
        elif verification_type == VerificationType.EMPLOYMENT:
            is_verified, details = self.verify_employment(data)
        else:
            return {
                "error": f"Unsupported verification type: {verification_type}",
                "data_hash": data_hash
            }
        
        print(f"Verification result: {is_verified}, Details: {details}")
        
        # Simulate oracle delay
        time.sleep(1)
        
        try:
            # Store result on blockchain
            tx_hash = self.blockchain.store_verification_result(
                data_hash=data_hash,
                is_verified=is_verified,
                verification_type=verification_type,
                details=details,
                account=self.blockchain.default_account  # Explicitly specify the account
            )
            
            print(f"Stored verification on blockchain with tx: {tx_hash}")
            
            # Confirm it was stored
            exists_after = self.blockchain.verification_exists(data_hash)
            print(f"Verification exists after storing: {exists_after}")
            
            # Return result with transaction details
            return {
                "data": data,
                "data_hash": data_hash,
                "is_verified": is_verified,
                "verification_type": verification_type.name,
                "details": details,
                "timestamp": int(datetime.now().timestamp()),
                "tx_hash": tx_hash,
                "status": "new"
            }
        except Exception as e:
            print(f"Error storing verification result: {e}")
            return {
                "error": f"Failed to store verification: {str(e)}",
                "data_hash": data_hash,
                "is_verified": is_verified,
                "details": details,
                "data": data
            }
    
    def close(self):
        """Close database connections."""
        if hasattr(self, 'db'):
            self.db.close()

# Example usage
if __name__ == "__main__":
    oracle = OracleSimulator()
    
    print("Oracle simulator initialized")
    
    # Example: Verify GPA
    gpa_data = {
        "name": "Kalana De Alwis",
        "university": "NSBM Green University",
        "gpa": 3.73
    }
    
    print("\nPerforming GPA verification...")
    gpa_result = oracle.verify_and_store_on_blockchain(gpa_data, VerificationType.GPA)
    print("\nGPA Verification Result:")
    print(json.dumps(gpa_result, indent=2))
    
    # Example: Verify Degree
    degree_data = {
        "name": "Kalana De Alwis",
        "university": "NSBM Green University",
        "degree": "BSc in Software Engineering" 
    }
    
    print("\nPerforming Degree verification...")
    degree_result = oracle.verify_and_store_on_blockchain(degree_data, VerificationType.DEGREE)
    print("\nDegree Verification Result:")
    print(json.dumps(degree_result, indent=2))
    
    # Example: Verify Employment
    employment_data = {
        "name": "Shehani Jayawardena",
        "company": "99X Technology",
        "job_title": "ML Engineer"
    }
    
    print("\nPerforming Employment verification...")
    employment_result = oracle.verify_and_store_on_blockchain(employment_data, VerificationType.EMPLOYMENT)
    print("\nEmployment Verification Result:")
    print(json.dumps(employment_result, indent=2))
    
    # Close connections
    oracle.close()
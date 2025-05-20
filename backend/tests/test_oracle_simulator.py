import unittest
import json
import time
from unittest.mock import patch, MagicMock

# Import the modules to be tested
from app.services.oracle_simulator import OracleSimulator, get_oracle

class TestOracleSimulator(unittest.TestCase):
    """
    Test suite for the Chainlink Oracle Simulator
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a new instance of OracleSimulator for each test
        self.oracle = OracleSimulator(oracle_address="0xTestOracleAddress")
        
        # Sample student/employee data
        self.student_data = {
            "student_id": "U117",
            "name": "Kalana De Alwis",
            "university": "NSBM Green University",
            "degree": "BSc in Software Engineering",
            "gpa": 3.73,
            "graduation_year": 2025
        }
        
        self.employment_data = {
            "employee_id": "E120",
            "name": "Shehani Jayawardena",
            "company": "99X Technology",
            "job_title": "ML Engineer",
            "job_category": "Machine Learning",
            "start_date": "2022-05-01",
            "end_date": "2023-11-01",
            "description": "Built NLP models for document processing and chatbot support."
        }
        
        self.resume_data = {
            "applicant_name": "Kalana De Alwis",
            "email": "kalana.dealwis@example.com",
            "phone": "+94771234567",
            "education": [
                {
                    "university": "NSBM Green University",
                    "degree": "BSc in Software Engineering",
                    "gpa": 3.73,
                    "graduation_year": 2025
                }
            ],
            "employment": [
                {
                    "company": "99X Technology",
                    "job_title": "ML Engineer",
                    "job_category": "Machine Learning",
                    "start_date": "2022-05-01",
                    "end_date": "2023-11-01",
                    "description": "Built NLP models for document processing and chatbot support."
                }
            ],
            "skills": ["Python", "Machine Learning", "NLP", "MongoDB"]
        }
    
    @patch('app.services.oracle_simulator.fetch_university_data_by_student_name')
    def test_verify_gpa_success(self, mock_fetch_university):
        """Test GPA verification when data matches"""
        # Mock the database fetch to return our sample student data
        mock_fetch_university.return_value = self.student_data
        
        # Test GPA verification with matching GPA
        result = self.oracle.verify_gpa("Kalana De Alwis", 3.73)
        
        # Assertions
        self.assertTrue(result["verified"])
        self.assertEqual(result["claimed_value"], 3.73)
        self.assertEqual(result["database_value"], 3.73)
        self.assertTrue("blockchain_data" in result)
        self.assertEqual(result["blockchain_data"]["verification_type"], "GPA_VERIFICATION")
    
    @patch('app.services.oracle_simulator.fetch_university_data_by_student_name')
    def test_verify_gpa_failure(self, mock_fetch_university):
        """Test GPA verification when data doesn't match"""
        # Mock the database fetch to return our sample student data
        mock_fetch_university.return_value = self.student_data
        
        # Test GPA verification with non-matching GPA
        result = self.oracle.verify_gpa("Kalana De Alwis", 3.5)
        
        # Assertions
        self.assertFalse(result["verified"])
        self.assertEqual(result["claimed_value"], 3.5)
        self.assertEqual(result["database_value"], 3.73)
    
    @patch('app.services.oracle_simulator.fetch_university_data_by_student_name')
    def test_verify_gpa_student_not_found(self, mock_fetch_university):
        """Test GPA verification when student not found"""
        # Mock the database fetch to return None (student not found)
        mock_fetch_university.return_value = None
        
        # Test GPA verification with a non-existent student
        result = self.oracle.verify_gpa("Non Existent Student", 3.73)
        
        # Assertions
        self.assertFalse(result["verified"])
        self.assertEqual(result["claimed_value"], 3.73)
        self.assertIsNone(result["database_value"])
        self.assertIn("No university record found", result["reason"])
    
    @patch('app.services.oracle_simulator.fetch_university_data_by_student_name')
    def test_verify_degree_success(self, mock_fetch_university):
        """Test degree verification when data matches"""
        # Mock the database fetch to return our sample student data
        mock_fetch_university.return_value = self.student_data
        
        # Test degree verification with matching university and degree
        result = self.oracle.verify_degree(
            "Kalana De Alwis",
            "NSBM Green University",
            "BSc in Software Engineering"
        )
        
        # Assertions
        self.assertTrue(result["verified"])
        self.assertEqual(result["claimed_values"]["university"], "NSBM Green University")
        self.assertEqual(result["claimed_values"]["degree"], "BSc in Software Engineering")
        self.assertEqual(result["database_values"]["university"], "NSBM Green University")
        self.assertEqual(result["database_values"]["degree"], "BSc in Software Engineering")
    
    @patch('app.services.oracle_simulator.fetch_university_data_by_student_name')
    def test_verify_degree_university_mismatch(self, mock_fetch_university):
        """Test degree verification when university doesn't match"""
        # Mock the database fetch to return our sample student data
        mock_fetch_university.return_value = self.student_data
        
        # Test verification with non-matching university
        result = self.oracle.verify_degree(
            "Kalana De Alwis",
            "University of Colombo",
            "BSc in Software Engineering"
        )
        
        # Assertions
        self.assertFalse(result["verified"])
        self.assertEqual(result["claimed_values"]["university"], "University of Colombo")
        self.assertEqual(result["database_values"]["university"], "NSBM Green University")
    
    @patch('app.services.oracle_simulator.fetch_company_data_by_employee_name')
    def test_verify_employment_success(self, mock_fetch_company):
        """Test employment verification when data matches"""
        # Mock the database fetch to return our sample employment data
        mock_fetch_company.return_value = [self.employment_data]
        
        # Test employment verification with matching company and job title
        result = self.oracle.verify_employment(
            "Shehani Jayawardena",
            "99X Technology",
            "ML Engineer"
        )
        
        # Assertions
        self.assertTrue(result["verified"])
        self.assertEqual(result["claimed_values"]["company"], "99X Technology")
        self.assertEqual(result["claimed_values"]["job_title"], "ML Engineer")
        self.assertEqual(result["database_values"]["company"], "99X Technology")
        self.assertEqual(result["database_values"]["job_title"], "ML Engineer")
    
    @patch('app.services.oracle_simulator.fetch_company_data_by_employee_name')
    def test_verify_employment_job_mismatch(self, mock_fetch_company):
        """Test employment verification when job title doesn't match"""
        # Mock the database fetch to return our sample employment data
        mock_fetch_company.return_value = [self.employment_data]
        
        # Test verification with non-matching job title
        result = self.oracle.verify_employment(
            "Shehani Jayawardena",
            "99X Technology",
            "Software Engineer"
        )
        
        # Assertions
        self.assertFalse(result["verified"])
        self.assertEqual(result["claimed_values"]["job_title"], "Software Engineer")
        # Should return database values as list since there's no exact match
        self.assertIsInstance(result["database_values"], list)
    
    @patch('app.services.oracle_simulator.fetch_company_data_by_employee_name')
    def test_verify_employment_employee_not_found(self, mock_fetch_company):
        """Test employment verification when employee not found"""
        # Mock the database fetch to return empty list (employee not found)
        mock_fetch_company.return_value = []
        
        # Test employment verification with a non-existent employee
        result = self.oracle.verify_employment(
            "Non Existent Employee",
            "99X Technology",
            "ML Engineer"
        )
        
        # Assertions
        self.assertFalse(result["verified"])
        self.assertIsNone(result["database_values"])
        self.assertIn("No employment records found", result["reason"])
    
    @patch('app.services.oracle_simulator.OracleSimulator.verify_gpa')
    @patch('app.services.oracle_simulator.OracleSimulator.verify_degree')
    @patch('app.services.oracle_simulator.OracleSimulator.verify_employment')
    def test_verify_complete_resume(self, mock_verify_employment, mock_verify_degree, mock_verify_gpa):
        """Test complete resume verification process"""
        # Mock individual verification methods to return predefined results
        mock_verify_gpa.return_value = {
            "verified": True,
            "reason": "GPA verified successfully",
            "claimed_value": 3.73,
            "database_value": 3.73,
            "blockchain_data": {
                "transaction_hash": "0xGPAHash",
                "data_hash": "0xDataHash1",
                "is_verified": True,
                "verification_type": "GPA_VERIFICATION",
                "timestamp": int(time.time()),
                "oracle_id": "ChainlinkOracleSim_v1"
            }
        }
        
        mock_verify_degree.return_value = {
            "verified": True,
            "reason": "Both university and degree verified successfully",
            "claimed_values": {
                "university": "NSBM Green University",
                "degree": "BSc in Software Engineering"
            },
            "database_values": {
                "university": "NSBM Green University",
                "degree": "BSc in Software Engineering"
            },
            "verification_details": {
                "university": "String values match",
                "degree": "String values match"
            },
            "blockchain_data": {
                "transaction_hash": "0xDegreeHash",
                "data_hash": "0xDataHash2",
                "is_verified": True,
                "verification_type": "DEGREE_VERIFICATION",
                "timestamp": int(time.time()),
                "oracle_id": "ChainlinkOracleSim_v1"
            }
        }
        
        mock_verify_employment.return_value = {
            "verified": True,
            "reason": "Employment details match company records",
            "claimed_values": {
                "company": "99X Technology",
                "job_title": "ML Engineer"
            },
            "database_values": {
                "company": "99X Technology",
                "job_title": "ML Engineer",
                "start_date": "2022-05-01",
                "end_date": "2023-11-01"
            },
            "blockchain_data": {
                "transaction_hash": "0xEmploymentHash",
                "data_hash": "0xDataHash3",
                "is_verified": True,
                "verification_type": "EMPLOYMENT_VERIFICATION",
                "timestamp": int(time.time()),
                "oracle_id": "ChainlinkOracleSim_v1"
            }
        }
        
        # Test complete resume verification
        result = self.oracle.verify_complete_resume(self.resume_data)
        
        # Assertions
        self.assertEqual(result["applicant_name"], "Kalana De Alwis")
        self.assertEqual(result["overall_status"], "VERIFIED")
        self.assertEqual(len(result["education_verification"]), 2)  # GPA and degree
        self.assertEqual(len(result["employment_verification"]), 1)  # One job
        self.assertIn("blockchain_status", result)
        self.assertIn("verification_id", result)
    
    def test_get_oracle_singleton(self):
        """Test that get_oracle returns the same instance"""
        oracle1 = get_oracle()
        oracle2 = get_oracle()
        self.assertIs(oracle1, oracle2)  # Should be same instance
    
    def test_verification_history(self):
        """Test that verification history is recorded correctly"""
        # Initially history should be empty
        self.assertEqual(len(self.oracle.get_verification_history()), 0)
        
        # Mock a verification to record in history
        data_hash = "0xTestDataHash"
        tx_hash = "0xTestTxHash"
        
        self.oracle._record_verification(
            data_hash=data_hash,
            verified=True,
            verification_type="TEST_VERIFICATION",
            tx_hash=tx_hash
        )
        
        # Check history has one record now
        history = self.oracle.get_verification_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["data_hash"], data_hash)
        self.assertEqual(history[0]["transaction_hash"], tx_hash)
        self.assertEqual(history[0]["verification_type"], "TEST_VERIFICATION")


if __name__ == '__main__':
    unittest.main()
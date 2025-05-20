# test_mock_db.py
import pytest
import sys
import os
from pprint import pprint

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions from mock_db.py
from app.services.mock_db import (
    fetch_university_data_by_student_name,
    fetch_company_data_by_employee_name,
    verify_student_gpa,
    verify_employment_history,
    DatabaseConnection
)

def test_database_connection():
    """Test that database connection can be established"""
    try:
        db_conn = DatabaseConnection()
        assert db_conn is not None
        university_collection = db_conn.get_university_collection()
        company_collection = db_conn.get_company_collection()
        assert university_collection is not None
        assert company_collection is not None
        print("✅ Database connection test passed")
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        raise

def test_fetch_university_data():
    """Test fetching university data for existing and non-existing students"""
    # Test with an existing student
    sample_student = "Nadeesha Alwis"  # Use a name you know exists in your DB
    result = fetch_university_data_by_student_name(sample_student)
    if result:
        print(f"✅ Successfully retrieved university data for {sample_student}:")
        pprint(result)
        assert "student_id" in result
        assert "name" in result
        assert "university" in result
        assert "degree" in result
        assert "gpa" in result
    else:
        print(f"❌ No data found for {sample_student}. Check if this student exists in your database.")
    
    # Test with a non-existing student
    non_existent = "NonExistentStudent12345"
    result = fetch_university_data_by_student_name(non_existent)
    assert result is None
    print(f"✅ Correctly returned None for non-existent student {non_existent}")

def test_fetch_company_data():
    """Test fetching company data for existing and non-existing employees"""
    # Test with an existing employee
    sample_employee = "Shehani Jayawardena"  # Use a name you know exists in your DB
    results = fetch_company_data_by_employee_name(sample_employee)
    if results:
        print(f"✅ Successfully retrieved {len(results)} employment record(s) for {sample_employee}:")
        for i, record in enumerate(results, 1):
            print(f"\nRecord {i}:")
            pprint(record)
            assert "employee_id" in record
            assert "name" in record
            assert "company" in record
            assert "job_title" in record
    else:
        print(f"❌ No employment records found for {sample_employee}. Check if this employee exists in your database.")
    
    # Test with a non-existing employee
    non_existent = "NonExistentEmployee12345"
    results = fetch_company_data_by_employee_name(non_existent)
    assert len(results) == 0
    print(f"✅ Correctly returned empty list for non-existent employee {non_existent}")

def test_verify_student_gpa():
    """Test GPA verification functionality"""
    # Test with correct GPA
    student = "Kalana De Alwis"
    correct_gpa = 3.73  # Use the correct GPA from your DB
    result = verify_student_gpa(student, correct_gpa)
    if result["record"]:
        print(f"✅ GPA verification with correct GPA ({correct_gpa}):")
        pprint(result)
        assert result["verified"] is True
    else:
        print(f"❌ Student {student} not found for GPA verification test")
    
    # Test with incorrect GPA
    if result["record"]:
        incorrect_gpa = 3.5  # Use an incorrect GPA
        result = verify_student_gpa(student, incorrect_gpa)
        print(f"✅ GPA verification with incorrect GPA ({incorrect_gpa}):")
        pprint(result)
        assert result["verified"] is False

def test_verify_employment_history():
    """Test employment history verification functionality"""
    # Test with correct employment details
    employee = "Shehani Jayawardena"
    company = "99X Technology"
    job_title = "ML Engineer"
    result = verify_employment_history(employee, company, job_title)
    if result["record"] or "records_found" in result:
        print(f"✅ Employment verification with correct details:")
        pprint(result)
        if "record" in result and result["record"]:
            assert result["verified"] is True
    else:
        print(f"❌ Employee {employee} not found for employment verification test")
    
    # Test with incorrect employment details
    incorrect_job = "Software Developer"  # Use an incorrect job title
    result = verify_employment_history(employee, company, incorrect_job)
    print(f"✅ Employment verification with incorrect job title ({incorrect_job}):")
    pprint(result)
    assert result["verified"] is False

if __name__ == "__main__":
    print("Running tests for mock_db.py...")
    
    try:
        test_database_connection()
        test_fetch_university_data()
        test_fetch_company_data()
        test_verify_student_gpa()
        test_verify_employment_history()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")